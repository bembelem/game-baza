from datetime import datetime, timedelta, timezone

import jwt
from jwt import ExpiredSignatureError, DecodeError
from pwdlib import PasswordHash

from app.api.schemas.auth import UserRegisterRequest, UserLoginRequest
from app.api.schemas.users import UserPatch
from app.services.schemas.auth import UserAdd
from app.services.schemas.users import UserPrivate
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

    async def login_user(self, data: UserLoginRequest):
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

    async def register_user(self, data: UserRegisterRequest):
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

    async def update_user(self, user_id: int, data: UserPatch) -> UserPrivate:
        """Частичное обновление профиля. Пароль хешируется, если передан.

        Пустой PATCH (без полей) — просто возвращает текущего юзера.
        На дубликате email/username бросает соответствующее 409.
        """
        fields = data.model_dump(exclude_unset=True, exclude_none=True)
        print(fields)
        if "password" in fields:
            fields["hashed_password"] = self.hash_password(fields.pop("password"))

        async with async_session_maker() as session:
            repo = UserRepository(session)
            if not fields:
                # клиент прислал пустой PATCH — просто отдаём текущего
                return await repo.get_one_or_none(id=user_id)

            try:
                user = await repo.update_by_id(user_id, fields)
                await session.commit()
            except ObjectAlreadyExistsError as ex:
                if ex.constraint == "users_email_key":
                    raise EmailAlreadyExistsHTTPException()
                if ex.constraint == "users_username_key":
                    raise UsernameAlreadyExistsHTTPException()
                raise AppHTTPException()

            if user is None:
                # юзера с таким id уже нет — токен битый/устаревший
                raise IncorrectTokenHTTPException()
            return user

    async def delete_user(self, user_id: int) -> None:
        """Удаляет пользователя. Идемпотентно: если уже удалён — ничего страшного."""
        async with async_session_maker() as session:
            await UserRepository(session).delete_by_id(user_id)
            await session.commit()

    def decode_token(self, token) -> dict:
        try:
            res = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
        except (ExpiredSignatureError, DecodeError) as e:
            raise IncorrectTokenHTTPException
        return res
