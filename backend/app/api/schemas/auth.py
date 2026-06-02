"""View-схемы для auth-роутов — только то что в OpenAPI (request/response)."""
import re
from datetime import date
from typing import TypeAlias, Optional, Annotated

from pydantic import BaseModel, EmailStr, field_validator, model_validator, Field, ConfigDict, BeforeValidator, \
    AfterValidator

from app.exceptions import UserNotFoundHTTPException


# Переиспользуемые типы

def _parse_birthdate(value):
    if isinstance(value, str) and "." in value:
        day, month, year = value.split(".")
        return date(int(year), int(month), int(day))
    return value

def _validate_birthdate(value: date) -> date:
    if value > date.today():
        raise ValueError("Birthdate must be in the past")
    return value


PasswordStr = Annotated[
    str,
    Field(
        min_length=6,
        max_length=50,
        pattern=r"^(?=.*\d)(?=.*[!@#$%^&*()_\-+=\[\]{};:'\",.<>/?\\|`~]).+$",
        description="Минимум 6 символов, хотя бы одна цифра и один спецсимвол",
    ),
]

UsernameStr = Annotated[
    str,
    Field(
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_ ]+$",
        description="3-50 символов: латиница, цифры, подчёркивания, пробелы",
    ),
]

BirthDate = Annotated[
    date,
    BeforeValidator(_parse_birthdate),
    AfterValidator(_validate_birthdate),
    Field(description="Дата рождения (YYYY-MM-DD или DD.MM.YYYY)"),
]

# Схемы

class UserRegisterRequest(BaseModel):
    """Тело запроса POST /auth/register."""

    model_config = ConfigDict(regex_engine="python-re")

    username: UsernameStr
    email: EmailStr = Field(description="Email пользователя", max_length=100)
    birthdate: BirthDate
    password: PasswordStr

    @field_validator("birthdate")
    @classmethod
    def birthdate_in_past(cls, value: date) -> date:
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


class UserLoginRequest(BaseModel):
    """Тело запроса POST /auth/login."""

    model_config = ConfigDict(regex_engine="python-re")

    username: Optional[UsernameStr | None] = None
    email: EmailStr | None = None
    password: PasswordStr

    @model_validator(mode="after")
    def at_least_one_field(self) -> "UserLoginRequest":
        if not any([self.username, self.email]):
            raise ValueError("Необходимо указать либо username, либо email")
        return self

    @model_validator(mode="after")
    def username_validate(self) -> "UserLoginRequest":
        if self.username:
            if (len(self.username) < 3 or len(self.username) > 50 or
                not re.match(r"^[a-zA-Z0-9_ ]+$", self.username)):
                raise UserNotFoundHTTPException()
        return self

    @model_validator(mode="after")
    def password_validate(self) -> "UserLoginRequest":
        if self.password:
            if (len(self.password) < 6 or len(self.password) > 50 or
                    not re.match(r"^(?=.*\d)(?=.*[!@#$%^&*()_\-+=\[\]{};:'\",.<>/?\\|`~]).+$", self.password)):
                raise UserNotFoundHTTPException()
        return self

class Token(BaseModel):
    """Не используется напрямую (токен в cookie), но описывает формат если когда-нибудь будет в body."""
    access_token: str
    token_type: str = "cookie"
