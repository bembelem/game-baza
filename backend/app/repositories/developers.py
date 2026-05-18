from sqlalchemy import select

from app.repositories.base import BaseRepository
from app.repositories.mappers.mappers import GameDataMapper
from database.models.catalogs import DeveloperOrm, PublisherOrm
from database.models.games import GameOrm, RawOfferOrm


class DeveloperRepository(BaseRepository):
    model = GameOrm
    mapper = GameDataMapper

    async def get_or_create_developer(
            self,
            name: str | None,
    ) -> DeveloperOrm | None:
        if not name:
            return None
        result = await self.session.execute(
            select(DeveloperOrm).where(DeveloperOrm.name == name)
        )
        dev = result.scalar_one_or_none()
        if not dev:
            dev = DeveloperOrm(name=name)
            self.session.add(dev)
            await self.session.flush()
        return dev