from typing import Type, TypeVar

from pydantic import BaseModel

from app.api.schemas.games import Game
from app.api.schemas.offers import Offer
from app.api.schemas.users import User
from database.database import Base
from database.models.games import GameOrm, OfferOrm
from database.models.users import UserOrm

SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper:
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
    schema = User


class GameDataMapper(DataMapper):
    db_model = GameOrm
    schema = Game


class OfferDataMapper(DataMapper):
    db_model = OfferOrm
    schema = Offer
