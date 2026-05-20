from sqlalchemy import select, func, and_, exists
from sqlalchemy.orm import selectinload

from app.api.schemas.games import GameFilters
from app.repositories.base import BaseRepository
from app.repositories.mappers import GameDataMapper
from database.models.catalogs import (
    DeveloperOrm,
    GenreOrm,
    PlatformOrm,
    PublisherOrm,
    StoreOrm,
    genres_games,
    platforms_games,
)
from database.models.games import GameOrm, OfferOrm, RawOfferOrm


class GameRepository(BaseRepository):
    model = GameOrm
    mapper = GameDataMapper

    async def get_or_create_batch(self, titles: list[str]) -> dict[str, int]:
        stmt = select(GameOrm.id, GameOrm.normalized_title).where(
            GameOrm.normalized_title.in_(titles)
        )
        result = await self.session.execute(stmt)
        title_to_id = {row.normalized_title: row.id for row in result}

        missing = [t for t in titles if t not in title_to_id]
        if missing:
            new_games = [GameOrm(normalized_title=t, title=t) for t in missing]
            self.session.add_all(new_games)
            await self.session.flush()
            for game in new_games:
                title_to_id[game.normalized_title] = game.id

        return title_to_id

    async def get_or_create_game(
            self,
            raw: RawOfferOrm,
            developer: DeveloperOrm | None,
            publisher: PublisherOrm | None,
    ) -> GameOrm:
        result = await self.session.execute(
            select(GameOrm).where(GameOrm.title == raw.title)
        )
        game = result.scalar_one_or_none()
        if game:
            return game

        game = GameOrm(
            title=raw.title,
            normalized_title=raw.normalized_title,
            description=raw.description,
            image_url=raw.image_url,
            release_date=raw.released,
            developer_id=developer.id if developer else None,
            publisher_id=publisher.id if publisher else None,
        )
        self.session.add(game)
        await self.session.flush()
        return game

    # list / page

    async def list_page(
        self, filters: GameFilters, last_id: int, per_page: int
    ) -> tuple[list[dict], int]:
        """Список игр с агрегированной минимальной ценой и общим count.

        Возвращает (items, total). items — список словарей с полями
        Game-схемы. total — общее количество подходящих под фильтры игр.
        """
        # Подзапрос: для каждой игры — min цены по офферам, учитывая фильтр магазинов.
        offer_q = (
            select(
                OfferOrm.game_id.label("game_id"),
                func.min(OfferOrm.price_original).label("min_orig"),
                func.min(OfferOrm.price_discount).label("min_disc"),
            )
            .group_by(OfferOrm.game_id)
        )
        if filters.stores:
            offer_q = offer_q.join(StoreOrm, StoreOrm.id == OfferOrm.store_id).where(
                StoreOrm.name.in_(filters.stores)
            )
        offer_sub = offer_q.subquery()

        # Базовый select по играм, JOIN с агрегатами по офферам.
        base = (
            select(
                GameOrm.id,
                GameOrm.title,
                GameOrm.image_url,
                offer_sub.c.min_orig,
                offer_sub.c.min_disc,
            )
            .join(offer_sub, offer_sub.c.game_id == GameOrm.id)
        )

        # Фильтры
        conditions = []
        if filters.title:
            # ILIKE с % в конце — prefix match, case-insensitive ('c' → 'Cyberpunk', 'Counter-Strike')
            conditions.append(GameOrm.title.ilike(f"{filters.title}%"))

        if filters.genres:
            for genre_name in filters.genres:
                conditions.append(
                    exists().where(
                        and_(
                            genres_games.c.game_id == GameOrm.id,
                            genres_games.c.genre_id == GenreOrm.id,
                            GenreOrm.name == genre_name,
                        )
                    )
                )

        # игра должна поддерживать ВСЕ выбранные платформы.
        if filters.platforms:
            for platform_name in filters.platforms:
                conditions.append(
                    exists().where(
                        and_(
                            platforms_games.c.game_id == GameOrm.id,
                            platforms_games.c.platform_id == PlatformOrm.id,
                            PlatformOrm.name == platform_name,
                        )
                    )
                )

        if filters.price_min is not None:
            conditions.append(offer_sub.c.min_disc >= filters.price_min)
        if filters.price_max is not None:
            conditions.append(offer_sub.c.min_disc <= filters.price_max)

        if conditions:
            base = base.where(and_(*conditions))

        # total — считаем ДО пагинации
        total_stmt = select(func.count()).select_from(base.subquery())
        total = (await self.session.execute(total_stmt)).scalar_one()

        # Сортировка
        sort_map = {
            "price_asc":  offer_sub.c.min_disc.asc(),
            "price_desc": offer_sub.c.min_disc.desc(),
            "title_asc":  GameOrm.title.asc(),
            "title_desc": GameOrm.title.desc(),
        }
        order_clause = sort_map.get(filters.sort, GameOrm.id.asc())

        # Cursor pagination: id > last_id — работает для default-сортировки.
        # Для price/title-сортировок это не идеальный курсор (могут дублироваться
        # элементы между страницами), но для MVP сойдёт.
        paged = (
            base.where(GameOrm.id > last_id)
            .order_by(order_clause, GameOrm.id.asc())
            .limit(per_page)
        )

        rows = (await self.session.execute(paged)).all()

        items = [
            {
                "id": row.id,
                "title": row.title,
                "image_url": row.image_url or "",
                "min_price_original": row.min_orig or 0,
                "min_price_discount": row.min_disc or 0,
                "discount_percent": _calc_discount(row.min_orig, row.min_disc),
            }
            for row in rows
        ]
        return items, total

    # Details

    async def get_details(self, game_id: int) -> GameOrm | None:
        stmt = (
            select(GameOrm)
            .options(
                selectinload(GameOrm.developer),
                selectinload(GameOrm.publisher),
                selectinload(GameOrm.genres),
                # offers + store одним loader-цепочкой → store.name доступен в сервисе
                selectinload(GameOrm.offers).selectinload(OfferOrm.store),
            )
            .where(GameOrm.id == game_id)
        )
        return (await self.session.execute(stmt)).scalar_one_or_none()


def _calc_discount(original: int | None, discount: int | None) -> int:
    if not original or not discount or original <= 0:
        return 0
    if discount >= original:
        return 0
    return round((1 - discount / original) * 100)
