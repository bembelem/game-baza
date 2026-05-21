from datetime import date

from pydantic import BaseModel, EmailStr


class UserAdd(BaseModel):
    """Данные для INSERT в БД при регистрации (после хеширования пароля)."""
    username: str
    email: EmailStr
    hashed_password: str
    birthdate: date


class UserWithHashedPassword(BaseModel):
    """Юзер с хешем — для аутентификации в login_user (verify_password)."""
    id: int
    hashed_password: str
    email: EmailStr
    birthdate: date
    username: str
    created_at: date
