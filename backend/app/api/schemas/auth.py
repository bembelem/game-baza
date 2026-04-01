from datetime import date

from pydantic import BaseModel, field_validator, EmailStr, model_validator

# Данные от клиента при регистрации (содержит сырой пароль)
class UserRequestAdd(BaseModel):
    username: str
    email: EmailStr
    birthdate: date
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "username": "john_doe",
                "email": "john@example.com",
                "birthdate": "2000-01-01",
                "password": "securepassword123"
            }]
        }
    }

    @field_validator("birthdate")
    @classmethod
    def birthdate_in_path(cls, value: date):
        if value > date.today():
            raise ValueError("Birthdate must be in the past")
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