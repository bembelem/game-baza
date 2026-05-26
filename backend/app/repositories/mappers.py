"""Мапперы между ORM-моделями и Pydantic-схемами."""
from typing import Type, TypeVar

from pydantic import BaseModel

from app.services.schemas.offers import Offer
from app.services.schemas.users import UserPrivate
from database.database import Base
from database.models.games import OfferOrm
from database.models.users import UserOrm

SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper:
    """Общий базовый mapper: ORM ↔ Pydantic через `model_validate`."""
    db_model: Type[Base]
    schema: Type[SchemaType]

    @classmethod
    def map_to_domain_entity(cls, data):
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data: BaseModel) -> Base:
        return cls.db_model(**data.model_dump())


class UserDataMapper(DataMapper):
    db_model = UserOrm
    schema = UserPrivate


class OfferDataMapper(DataMapper):
    db_model = OfferOrm
    schema = Offer
