import re
from datetime import date

from pydantic import BaseModel, field_validator, EmailStr, model_validator


# Данные от клиента при регистрации (содержит сырой пароль)
class UserRequestAdd(BaseModel):
    username: str
    email: EmailStr
    birthdate: date
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str):
        if len(value) < 3:
            raise ValueError("Username must be at least 3 characters")
        if len(value) > 50:
            raise ValueError("Username must be at most 50 characters")
        if not re.match(r"^[a-zA-Z0-9_ ]+$", value):
            raise ValueError("Username can only contain letters, digits, underscores and whitespaces")
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[0-9]", value):
            raise ValueError("Password must contain at least one digit")
        return value

    @field_validator("birthdate")
    @classmethod
    def birthdate_in_path(cls, value: date):
        if value > date.today():
            raise ValueError("Birthdate must be in the past")
        return value

    @field_validator("birthdate", mode="before")
    @classmethod
    def parse_birthdate(cls, value):
        if isinstance(value, str) and "." in value:
            day, month, year = value.split(".")
            return date(int(year), int(month), int(day))
        return value


# Данные для записи в БД (пароль уже захеширован)
class UserAdd(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    birthdate: date


class UserWithHashedPassword(BaseModel):
    id: int
    hashed_password: str
    email: EmailStr
    birthdate: date
    username: str
    created_at: date

# Данные от клиента при логине (можно войти через email или username)
class UserRequestLogin(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str

    @model_validator(mode="after")
    def at_least_one_field(self) -> "UserRequestLogin":
        if not any([self.username, self.email]):
            raise ValueError("Необходимо указать либо username, либо email")
        return self

class Token(BaseModel):
    access_token: str
    token_type: str = "cookie"