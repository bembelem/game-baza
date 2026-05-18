from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import insert

from app.repositories.base import BaseRepository
from database.models.games import RawOfferOrm


class RawOfferRepository(BaseRepository):
    model = RawOfferOrm

    async def add_batch(self, raw_offers: list[dict]) -> None:
        stmt = insert(self.model).values(raw_offers)
        stmt = stmt.on_conflict_do_update(
            constraint="uq_raw_offer_store",
            set_={
                col.name: stmt.excluded[col.name]
                for col in self.model.__table__.columns
                if col.name not in ('id', 'title', 'store')
            }
        )
        await self.session.execute(stmt)
        await self.session.commit()