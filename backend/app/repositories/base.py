import logging
from typing import Any

from asyncpg.exceptions import UniqueViolationError
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Base
from app.exceptions import ObjectAlreadyExistsError
from app.repositories.mappers.base import DataMapper


class BaseRepository:
    model = type[Base]
    mapper: type[DataMapper]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel) -> BaseModel | Any:
        try:
            add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
            result = await self.session.execute(add_data_stmt)
            model = result.scalars().one()
            return self.mapper.map_to_domain_entity(model)
        except IntegrityError as ex:
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                constraint = getattr(ex.orig.__cause__, "constraint_name", None)
                raise ObjectAlreadyExistsError(constraint=constraint) from ex