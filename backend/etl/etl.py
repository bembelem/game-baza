"""ETL: raw_offers → games / offers / catalogs (нормализованные данные).

Запускается отдельным процессом (cron / вручную) после Scrapy.
Идемпотентен: повторный запуск над теми же raw'ами просто пометит их as processed.
"""
import asyncio
import logging
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.database import async_session_maker
from database.models.catalogs import (
    DeveloperOrm,
    GenreOrm,
    PlatformOrm,
    PublisherOrm,
    StoreOrm,
)
from database.models.games import GameOrm, OfferOrm, RawOfferOrm
from utils.normalizers import normalize_genres, normalize_title, price_to_int

logger = logging.getLogger(__name__)

BATCH_SIZE = 100


async def run_etl() -> None:
    """Обрабатывает все необработанные raw_offers батчами."""
    logger.info("ETL started")
    total_processed = 0
    total_failed = 0

    while True:
        async with async_session_maker() as session:
            batch = await _fetch_unprocessed(session, BATCH_SIZE)
            if not batch:
                break

            for raw in batch:
                try:
                    async with session.begin_nested():
                        await _process_one(session, raw)
                        raw.is_processed = True
                    total_processed += 1
                except Exception:
                    logger.exception(
                        "ETL failed for raw_offer id=%s title=%r store=%r",
                        raw.id, raw.title, raw.store,
                    )
                    total_failed += 1
                    continue

            await session.commit()

    logger.info(
        "ETL finished. processed=%d failed=%d", total_processed, total_failed
    )


# batch fetch

async def _fetch_unprocessed(session: AsyncSession, limit: int) -> list[RawOfferOrm]:
    result = await session.execute(
        select(RawOfferOrm)
        .where(RawOfferOrm.is_processed.is_(False))
        .order_by(RawOfferOrm.id)
        .limit(limit)
    )
    return list(result.scalars().all())


# основной конвейер

async def _process_one(session: AsyncSession, raw: RawOfferOrm) -> None:
    """Нормализует один raw_offer в Game + Offer (+ справочники)."""
    store = await _get_or_create_store(session, raw.store)
    developer = await _get_or_create_developer(session, raw.developer)
    publisher = await _get_or_create_publisher(session, raw.publisher)

    normalized_genre_names = normalize_genres(raw.genres or [])
    genres = await _get_or_create_genres(session, normalized_genre_names)
    platforms = await _get_or_create_platforms(session, raw.platforms or [])

    game = await _get_or_create_game(
        session,
        raw=raw,
        developer=developer,
        publisher=publisher,
        genres=genres,
        platforms=platforms,
    )

    await _upsert_offer(session, raw=raw, game=game, store=store)


# справочники

async def _get_or_create_store(session: AsyncSession, name: str) -> StoreOrm:
    return await _get_or_create_named(session, StoreOrm, name)


async def _get_or_create_developer(
    session: AsyncSession, name: str | None
) -> DeveloperOrm | None:
    if not name:
        return None
    return await _get_or_create_named(session, DeveloperOrm, name)


async def _get_or_create_publisher(
    session: AsyncSession, name: str | None
) -> PublisherOrm | None:
    if not name:
        return None
    return await _get_or_create_named(session, PublisherOrm, name)


async def _get_or_create_genres(
    session: AsyncSession, names: Iterable[str]
) -> list[GenreOrm]:
    return [await _get_or_create_named(session, GenreOrm, n) for n in names]


async def _get_or_create_platforms(
    session: AsyncSession, names: Iterable[str]
) -> list[PlatformOrm]:
    return [await _get_or_create_named(session, PlatformOrm, n) for n in names if n]


async def _get_or_create_named(session: AsyncSession, model, name: str):
    """Универсальный get-or-create для справочников с уникальным `name`."""
    name = name.strip()
    result = await session.execute(select(model).where(model.name == name))
    obj = result.scalar_one_or_none()
    if obj is not None:
        return obj
    obj = model(name=name)
    session.add(obj)
    # flush, а не commit: чтобы получить id, но оставить транзакцию открытой
    await session.flush()
    return obj


# games

async def _get_or_create_game(
    session: AsyncSession,
    *,
    raw: RawOfferOrm,
    developer: DeveloperOrm | None,
    publisher: PublisherOrm | None,
    genres: list[GenreOrm],
    platforms: list[PlatformOrm],
) -> GameOrm:
    """Ищет игру по normalized_title, создаёт если нет.

    Несколько raw_offers из разных магазинов могут описывать одну игру
    (например, Cyberpunk 2077 в GabeStore и SteamBuy).
    Дедупликация — по normalized_title.
    """
    normalized = raw.normalized_title or normalize_title(raw.title)

    # selectinload — eager-load M2M, иначе обращение к game.genres / game.platforms
    # ниже триггернёт lazy load и упадёт с MissingGreenlet в async-сессии.
    result = await session.execute(
        select(GameOrm)
        .options(
            selectinload(GameOrm.genres),
            selectinload(GameOrm.platforms),
        )
        .where(GameOrm.normalized_title == normalized)
    )
    game = result.scalar_one_or_none()

    if game is not None:
        # обогащаем уже существующую игру тем, чего у неё не было
        if not game.description and raw.description:
            game.description = raw.description
        if not game.release_date and raw.released:
            game.release_date = raw.released
        if not game.image_url and raw.image_url:
            game.image_url = raw.image_url
        if game.developer_id is None and developer is not None:
            game.developer = developer
        if game.publisher_id is None and publisher is not None:
            game.publisher = publisher
        _merge_m2m(game.genres, genres)
        _merge_m2m(game.platforms, platforms)
        return game

    game = GameOrm(
        title=raw.title,
        normalized_title=normalized,
        description=raw.description,
        release_date=raw.released,
        image_url=raw.image_url,
        developer=developer,
        publisher=publisher,
        genres=list(genres),
        platforms=list(platforms),
    )
    session.add(game)
    await session.flush()
    return game


def _merge_m2m(existing: list, incoming: Iterable) -> None:
    """Добавляет в M2M-коллекцию элементы, которых там ещё нет (по id)."""
    existing_ids = {obj.id for obj in existing if obj.id is not None}
    for obj in incoming:
        if obj.id not in existing_ids:
            existing.append(obj)


# offers

async def _upsert_offer(
    session: AsyncSession,
    *,
    raw: RawOfferOrm,
    game: GameOrm,
    store: StoreOrm,
) -> OfferOrm:
    """Создаёт новый оффер либо обновляет существующий (по UQ title+store_id).

    OfferOrm хранит снапшот raw-полей (developer/publisher/genres строками) —
    это сделано осознанно: позволяет отдавать карточку магазина «как было»,
    даже если справочники изменятся.
    """
    result = await session.execute(
        select(OfferOrm).where(
            OfferOrm.title == raw.title,
            OfferOrm.store_id == store.id,
        )
    )
    offer = result.scalar_one_or_none()

    price_original = price_to_int(raw.price_original)
    price_discount = price_to_int(raw.price_discount)
    normalized = raw.normalized_title or normalize_title(raw.title)

    if offer is None:
        offer = OfferOrm(
            title=raw.title,
            normalized_title=normalized,
            description=raw.description,
            released=raw.released,
            image_url=raw.image_url,
            link=raw.link,
            reviews_count=raw.reviews_count,
            positive_percent=raw.positive_percent,
            game_id=game.id,
            store_id=store.id,
            developer=raw.developer,
            publisher=raw.publisher,
            platforms=_join_or_none(raw.platforms),
            genres=_join_or_none(raw.genres),
            store_game_link=raw.link,
            price_original=price_original,
            price_discount=price_discount,
            discount_percent=raw.discount_percent,
        )
        session.add(offer)
    else:
        # обновляем «живые» поля (цены, отзывы, скидки)
        offer.price_original = price_original
        offer.price_discount = price_discount
        offer.discount_percent = raw.discount_percent
        offer.reviews_count = raw.reviews_count
        offer.positive_percent = raw.positive_percent
        # дозаполняем то, чего не было
        if not offer.description and raw.description:
            offer.description = raw.description
        if not offer.image_url and raw.image_url:
            offer.image_url = raw.image_url
        if not offer.link and raw.link:
            offer.link = raw.link
            offer.store_game_link = raw.link

    await session.flush()
    return offer


def _join_or_none(values: list[str] | None) -> str | None:
    if not values:
        return None
    return ", ".join(values)


# entry point

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    )
    asyncio.run(run_etl())
