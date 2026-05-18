from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app.repositories.base import BaseRepository
from app.repositories.mappers.mappers import OfferDataMapper
from database.models.games import OfferOrm, GameOrm


class OfferRepository(BaseRepository):
    model = OfferOrm
    mapper = OfferDataMapper

    async def add_batch(self, data: list[BaseModel]) -> None:
        stmt = insert(self.model).values([offer.model_dump() for offer in data])
        stmt = stmt.on_conflict_do_update(
            constraint="uq_game_store",
            set_={
                col.name: stmt.excluded[col.name]
                for col in self.model.__table__.columns
                if col.name not in ('id', 'title', 'store_id')
            }
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def get_id_by_normalized_title(self, normalized_title: str) -> int:
        stmt = select(GameOrm.id).where(GameOrm.normalized_title == normalized_title)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

# TODO: get_id_by_normalized_title - можно использовать get one or none из base