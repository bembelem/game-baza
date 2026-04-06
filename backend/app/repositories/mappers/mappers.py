from app.api.schemas.users import User
from app.models.users import UsersOrm
from app.repositories.mappers.base import DataMapper


class UsersDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User
