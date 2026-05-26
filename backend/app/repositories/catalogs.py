"""Репозитории справочников (genres, stores, platforms, publishers, developers)."""
from typing import Generic, TypeVar

from sqlalchemy import select

from app.repositories.base import BaseRepository
from database.database import Base
from database.models.catalogs import (
    DeveloperOrm,
    GenreOrm,
    PlatformOrm,
    PublisherOrm,
    StoreOrm,
)

M = TypeVar("M", bound=Base)


class CatalogRepository(BaseRepository, Generic[M]):
    model: type[M]

    async def list_all(self) -> list[M]:
        stmt = select(self.model).order_by(self.model.name)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, item_id: int) -> M | None:
        stmt = select(self.model).where(self.model.id == item_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class GenreRepository(CatalogRepository[GenreOrm]):
    model = GenreOrm


class StoreRepository(CatalogRepository[StoreOrm]):
    model = StoreOrm


class PlatformRepository(CatalogRepository[PlatformOrm]):
    model = PlatformOrm


class PublisherRepository(CatalogRepository[PublisherOrm]):
    model = PublisherOrm


class DeveloperRepository(CatalogRepository[DeveloperOrm]):
    model = DeveloperOrm
