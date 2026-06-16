"""Тесты качества данных, отдаваемых фронту после парсинга + ETL.
pytest tests/test_data_quality.py --integration
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app

# пороги для агрегатных проверок (доли по выборке)
SAMPLE_PAGES = 5          # сколько страниц каталога просматриваем
PER_PAGE = 20             # максимум по контракту (le=20)
MIN_PRICED_SHARE = 0.5    # доля карточек с ненулевой ценой (ловит баг «0 ₽ у всех»)
MIN_IMAGE_SHARE = 0.8     # доля карточек с http-картинкой
MIN_GENRES_SHARE = 0.7    # доля детальных карточек с непустыми жанрами
DETAILS_SAMPLE = 25       # сколько игр проверяем детально (с офферами)


@pytest.fixture(scope="module")
def client() -> TestClient:
    with TestClient(app) as c:
        yield c


def _fetch_page(client: TestClient, last_id: int = 0, per_page: int = PER_PAGE) -> dict:
    resp = client.get("/games", params={"last_id": last_id, "per_page": per_page})
    assert resp.status_code == 200, f"/games вернул {resp.status_code}: {resp.text[:300]}"
    return resp.json()


def _collect_cards(client: TestClient, max_pages: int = SAMPLE_PAGES) -> tuple[list[dict], list[list[dict]]]:
    """Проходит несколько страниц каталога. Возвращает (все карточки, страницы)."""
    cards: list[dict] = []
    pages: list[list[dict]] = []
    last_id, seen = 0, 0
    for _ in range(max_pages):
        page = _fetch_page(client, last_id=last_id)
        items = page["items"]
        pages.append(items)
        cards.extend(items)
        if not page["has_more"] or page["last_id"] is None:
            break
        last_id = page["last_id"]
        seen += len(items)
    return cards, pages


# Инварианты одной карточки каталога

def _assert_card_invariants(card: dict) -> None:
    cid = card.get("id")
    assert card["title"].strip(), f"[id={cid}] пустой title"
    assert card["image_url"] != "", f"[id={cid}] пустой image_url"

    orig = card["min_price_original"]
    disc = card["min_price_discount"]
    pct = card["discount_percent"]

    assert orig >= 0, f"[id={cid}] отрицательная original-цена: {orig}"
    assert disc >= 0, f"[id={cid}] отрицательная discount-цена: {disc}"
    assert disc <= orig, f"[id={cid}] цена со скидкой больше оригинала: {disc} > {orig}"
    assert 0 <= pct <= 100, f"[id={cid}] discount_percent вне 0..100: {pct}"
    # согласованность: есть скидка в % → цена реально ниже оригинала
    if pct > 0:
        assert disc < orig, f"[id={cid}] discount_percent={pct}, но disc={disc} == orig={orig}"


@pytest.mark.integration
class TestCatalogRecordQuality:
    """Качество карточек в ответе GET /games."""

    def test_catalog_not_empty(self, client: TestClient) -> None:
        """БД должна быть наполнена (иначе остальные проверки бессмысленны)."""
        page = _fetch_page(client)
        assert page["total"] > 0, "Каталог пуст — прогоните пауков и `python -m etl.etl`"
        assert page["items"], "total>0, но items пустой"

    def test_every_card_holds_invariants(self, client: TestClient) -> None:
        cards, _ = _collect_cards(client)
        assert cards, "не удалось собрать карточки"
        for card in cards:
            _assert_card_invariants(card)

    def test_prices_are_mostly_nonzero(self, client: TestClient) -> None:
        """Ловит регрессию «у всех игр 0 ₽» (например, когда цена не маппится в БД)."""
        cards, _ = _collect_cards(client)
        priced = [c for c in cards if c["min_price_discount"] > 0]
        share = len(priced) / len(cards)
        assert share >= MIN_PRICED_SHARE, (
            f"Только {share:.0%} карточек с ненулевой ценой "
            f"(порог {MIN_PRICED_SHARE:.0%}). Похоже, цена не доезжает до БД."
        )

    def test_images_are_mostly_valid_urls(self, client: TestClient) -> None:
        cards, _ = _collect_cards(client)
        with_img = [c for c in cards if c["image_url"].startswith(("http://", "https://"))]
        share = len(with_img) / len(cards)
        assert share >= MIN_IMAGE_SHARE, (
            f"Только {share:.0%} карточек с http-картинкой (порог {MIN_IMAGE_SHARE:.0%})."
        )


@pytest.mark.integration
class TestCatalogPagination:
    """Контракт пагинации — фронт ходит по last_id, повторов быть не должно."""

    def test_per_page_respected(self, client: TestClient) -> None:
        page = _fetch_page(client, per_page=PER_PAGE)
        assert len(page["items"]) <= PER_PAGE
        assert page["per_page"] == PER_PAGE

    def test_has_more_and_last_id_consistent(self, client: TestClient) -> None:
        page = _fetch_page(client)
        if page["has_more"]:
            assert page["last_id"] is not None, "has_more=True, но last_id=None"
            assert page["last_id"] == len(page["items"]), (
                "last_id должен быть offset'ом = числу уже отданных записей"
            )
        else:
            assert page["last_id"] is None, "has_more=False, но last_id задан"

    def test_no_duplicate_ids_across_pages(self, client: TestClient) -> None:
        """Главная регрессия пагинации: одна игра не должна приходить дважды."""
        cards, pages = _collect_cards(client)
        ids = [c["id"] for c in cards]
        assert len(ids) == len(set(ids)), "Дубли id между страницами каталога"
        # и внутри страницы тоже
        for i, items in enumerate(pages):
            page_ids = [c["id"] for c in items]
            assert len(page_ids) == len(set(page_ids)), f"Дубли id внутри страницы #{i}"


# Детальная карточка + офферы (GET /games/{id})

def _sample_game_ids(client: TestClient, n: int) -> list[int]:
    ids: list[int] = []
    last_id = 0
    while len(ids) < n:
        page = _fetch_page(client, last_id=last_id)  # стабильный порядок (id asc)
        items = page["items"]
        ids.extend(c["id"] for c in items)
        if not page["has_more"] or page["last_id"] is None:
            break
        last_id = page["last_id"]
    return ids[:n]


@pytest.mark.integration
class TestGameDetailsQuality:
    """Качество детальной карточки и офферов."""

    def test_details_hold_invariants(self, client: TestClient) -> None:
        ids = _sample_game_ids(client, DETAILS_SAMPLE)
        assert ids, "не удалось набрать id игр для детальной проверки"

        genres_present = 0
        for gid in ids:
            resp = client.get(f"/games/{gid}")
            assert resp.status_code == 200, f"/games/{gid} → {resp.status_code}"
            g = resp.json()

            assert g["title"].strip(), f"[id={gid}] пустой title"
            assert g["image_url"] != "", f"[id={gid}] пустой image_url"

            orig, disc, pct = g["min_price_original"], g["min_price_discount"], g["discount_percent"]
            assert disc <= orig, f"[id={gid}] disc {disc} > orig {orig}"
            assert 0 <= pct <= 100, f"[id={gid}] discount_percent {pct} вне 0..100"

            if g["genres"]:
                genres_present += 1

            offers = g["offers"]
            assert offers, f"[id={gid}] игра в каталоге, но без офферов"
            for off in offers:
                assert off["store"].strip(), f"[id={gid}] оффер без названия магазина"
                assert off["store_game_link"].startswith(("http://", "https://")), (
                    f"[id={gid}] битая ссылка оффера: {off['store_game_link']!r}"
                )
                o_orig, o_disc = off["price_original"], off["price_discount"]
                assert o_disc <= o_orig, f"[id={gid}] оффер: disc {o_disc} > orig {o_orig}"
                assert 0 <= off["discount_percent"] <= 100

            # min-цена карточки = минимум по офферам (согласованность агрегата)
            min_off_disc = min(o["price_discount"] for o in offers)
            assert disc == min_off_disc, (
                f"[id={gid}] min_price_discount={disc}, а минимум по офферам={min_off_disc}"
            )

        share = genres_present / len(ids)
        assert share >= MIN_GENRES_SHARE, (
            f"Только {share:.0%} игр с непустыми жанрами (порог {MIN_GENRES_SHARE:.0%})."
        )

    def test_unknown_game_returns_404(self, client: TestClient) -> None:
        resp = client.get("/games/999999999")
        assert resp.status_code == 404
