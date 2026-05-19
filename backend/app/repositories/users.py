from pydantic import EmailStr
from sqlalchemy import select

from app.api.schemas.auth import UserWithHashedPassword
from database.models.users import UserOrm
from app.repositories.base import BaseRepository
from app.repositories.mappers import UserDataMapper


class UserRepository(BaseRepository):
    model = UserOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr = None, username: str = None):
        if not (email or username):
            raise ValueError("Необходимо указать email или username")

        filters = {}
        if email:
            filters["email"] = email
        if username:
            filters["username"] = username

        query = select(self.model).filter_by(**filters)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserWithHashedPassword.model_validate(model, from_attributes=True)
