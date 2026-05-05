from datetime import datetime, timedelta, timezone

import jwt
from jwt import ExpiredSignatureError, DecodeError
from pwdlib import PasswordHash

from app.api.schemas.auth import UserRequestRegister, UserAdd, UserRequestLogin
from database.config import settings
from database.database import async_session_maker
from app.exceptions import EmailAlreadyExistsHTTPException, UsernameAlreadyExistsHTTPException, \
    EmailNotRegisteredHTTPException, UsernameNotRegisteredHTTPException, IncorrectPasswordHTTPException, \
    ObjectAlreadyExistsError, AppHTTPException, IncorrectTokenHTTPException
from app.repositories.users import UserRepository


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

    async def login_user(self, data: UserRequestLogin):
        async with async_session_maker() as session:
            if data.email:
                user = await UserRepository(session).get_user_with_hashed_password(email=data.email)
                if not user:
                    raise EmailNotRegisteredHTTPException()
            elif data.username:
                user = await UserRepository(session).get_user_with_hashed_password(username=data.username)
                if not user:
                    raise UsernameNotRegisteredHTTPException()
            if not self.verify_password(data.password, user.hashed_password):
                raise IncorrectPasswordHTTPException()
            return user

    async def register_user(self, data: UserRequestRegister):
        async with async_session_maker() as session:

            hashed_password = self.hash_password(data.password)
            new_user = UserAdd(
                username=data.username,
                email=data.email,
                birthdate=data.birthdate,
                hashed_password=hashed_password,
            )

            try:
                user = await UserRepository(session).add(new_user)
            except ObjectAlreadyExistsError as ex:
                if ex.constraint == "users_email_key":
                    raise EmailAlreadyExistsHTTPException()
                if ex.constraint == "users_username_key":
                    raise UsernameAlreadyExistsHTTPException()
                raise AppHTTPException()
            await session.commit()
            return user

    def decode_token(self, token) -> dict:
        try:
            res = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
        except (ExpiredSignatureError, DecodeError) as e:
            raise IncorrectTokenHTTPException
        return res
