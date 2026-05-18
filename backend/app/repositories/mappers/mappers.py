from app.api.schemas.games import Game
from app.api.schemas.offers import Offer
from app.api.schemas.users import User
from app.repositories.mappers.base import DataMapper
from database.models.games import OfferOrm, GameOrm, RawOfferOrm
from database.models.users import UserOrm


class UserDataMapper(DataMapper):
    db_model = UserOrm
    schema = User

class OfferDataMapper(DataMapper):
    db_model = OfferOrm
    schema = Offer

class GameDataMapper(DataMapper):
    db_model = GameOrm
    schema = Game
