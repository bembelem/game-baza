from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException
from pwdlib import PasswordHash

from app.api.schemas.auth import UserRequestAdd, UserAdd, UserRequestLogin
from app.config import settings
from app.database import async_session_maker
from app.exceptions import UserAlreadyExistsException, EmailNotRegisteredException, IncorrectPasswordException
from app.repositories.users import UsersRepository


class AuthService:
    password_hash = PasswordHash.recommended()

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    def verify_password(self, plain_password, hashed_password):
        return self.password_hash.verify(plain_password, hashed_password)

    def hash_password(self, password):
        return self.password_hash.hash(password)

    async def register_user(self, data: UserRequestAdd):
        async with async_session_maker() as session:
            existing_user = await UsersRepository(session).get_one_or_none(email=data.email)
            if existing_user:
                raise UserAlreadyExistsException()

            hashed_password = self.hash_password(data.password)
            new_user_data = data.model_dump()
            del new_user_data["password"]
            new_user_data["hashed_password"] = hashed_password
            new_user = UserAdd.model_validate(new_user_data)

            await UsersRepository(session).add(new_user)
            await session.commit()

    async def login_user(self, data: UserRequestLogin):
        async with async_session_maker() as session:
            user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
            if not user:
                raise EmailNotRegisteredException()
            if not self.verify_password(data.password, user.hashed_password):
                raise IncorrectPasswordException()
            return user