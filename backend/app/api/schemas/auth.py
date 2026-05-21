"""View-схемы для auth-роутов — только то что в OpenAPI (request/response)."""
import re
from datetime import date

from pydantic import BaseModel, EmailStr, field_validator, model_validator, Field, ConfigDict


class UserRegisterRequest(BaseModel):
    """Тело запроса POST /auth/register."""

    model_config = ConfigDict(regex_engine="python-re")

    username: str = Field(
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_ ]+$",
        description="3-50 символов: латиница, цифры, подчёркивания, пробелы",
    )
    email: EmailStr = Field(description="Email пользователя")
    birthdate: date = Field(description="Дата рождения (YYYY-MM-DD или DD.MM.YYYY)")
    password: str = Field(
        min_length=6,
        max_length=50,


        pattern=r"^(?=.*\d)(?=.*[!@#$%^&*()_\-+=\[\]{};:'\",.<>/?\\|`~]).+$",
        description="Минимум 6 символов, хотя бы одна цифра и один спецсимвол",
    )

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

    username: str | None = None
    email: EmailStr | None = None
    password: str

    @model_validator(mode="after")
    def at_least_one_field(self) -> "UserLoginRequest":
        if not any([self.username, self.email]):
            raise ValueError("Необходимо указать либо username, либо email")
        return self


class Token(BaseModel):
    """Не используется напрямую (токен в cookie), но описывает формат если когда-нибудь будет в body."""
    access_token: str
    token_type: str = "cookie"
