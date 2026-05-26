from app.api.schemas.games import (
    GameDetails,
    GamesResponse,
    ReviewsResponse,
)
from app.services.schemas.games import GameCard, GameFilters
from app.services.schemas.offers import Offer
from app.api.dependencies import PaginationParams
from app.exceptions import GameNotFoundHTTPException
from app.repositories.games import GameRepository, _calc_discount
from database.database import async_session_maker
from database.models.games import GameOrm, OfferOrm


class GamesService:

    async def get_games_page(
        self, filters: GameFilters, pagination: PaginationParams
    ) -> GamesResponse:
        async with async_session_maker() as session:
            items, total = await GameRepository(session).list_page(
                filters=filters,
                last_id=pagination.last_id,
                per_page=pagination.per_page,
            )

        games = [GameCard(**item) for item in items]
        last_id = games[-1].id if games else None
        # has_more: если набрали ровно per_page — потенциально есть ещё страница.
        # Точнее можно было бы LIMIT per_page+1, но для UX-страницы такой оценки достаточно.
        has_more = len(games) == pagination.per_page and total > pagination.last_id + len(games)

        return GamesResponse(
            total=total,
            last_id=last_id,
            per_page=pagination.per_page,
            has_more=has_more,
            items=games,
        )

    async def get_game_details(self, game_id: int) -> GameDetails:
        async with async_session_maker() as session:
            game = await GameRepository(session).get_details(game_id)

        if game is None:
            raise GameNotFoundHTTPException()

        return _game_to_details(game)

    async def get_reviews(self, game_id: int) -> ReviewsResponse:
        # Reviews как фича ещё не реализованы (нет таблицы).
        # Возвращаем пустой ответ, чтобы фронт мог рисовать секцию-заглушку.
        async with async_session_maker() as session:
            game = await GameRepository(session).get_details(game_id)
        if game is None:
            raise GameNotFoundHTTPException()
        return ReviewsResponse(reviews=[])


def _game_to_details(game: GameOrm) -> GameDetails:
    min_orig, min_disc = _aggregate_min_prices(game.offers)
    return GameDetails(
        id=game.id,
        title=game.title,
        image_url=game.image_url or "",
        min_price_original=min_orig,
        min_price_discount=min_disc,
        discount_percent=_calc_discount(min_orig, min_disc),
        description=game.description,
        release_date=game.release_date,
        developer=game.developer.name if game.developer else None,
        publisher=game.publisher.name if game.publisher else None,
        genres=[g.name for g in game.genres],
        offers=[_offer_to_schema(o) for o in game.offers],
    )


def _aggregate_min_prices(offers: list[OfferOrm]) -> tuple[int, int]:
    if not offers:
        return 0, 0
    originals = [o.price_original for o in offers if o.price_original is not None]
    discounts = [o.price_discount for o in offers if o.price_discount is not None]
    return min(originals) if originals else 0, min(discounts) if discounts else 0


def _offer_to_schema(offer: OfferOrm) -> Offer:
    # offer.store подгружено через selectinload в GameRepository.get_details
    return Offer(
        id=offer.id,
        game_id=offer.game_id,
        store_id=offer.store_id or 0,
        store=offer.store.name if offer.store else "",
        store_game_link=offer.store_game_link or offer.link or "",
        price_original=offer.price_original or 0,
        price_discount=offer.price_discount or 0,
        discount_percent=_percent_to_int(offer.discount_percent),
        positive_percent=offer.positive_percent or 0,
    )



def _percent_to_int(value: str | None) -> int:
    # В OfferOrm.discount_percent хранится строкой ('-50', '0', '' и т.п.)
    if not value:
        return 0
    digits = "".join(ch for ch in value if ch.isdigit())
    return int(digits) if digits else 0
