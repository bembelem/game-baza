from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator, model_validator
from backend.app.api.schemas.games import Game
from datetime import date


class User(BaseModel):
    id: int
    username: str
    birthdate: date
    email: str
    created_at: str
    wishlist_id: int

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "id": 1,
                "username": "john_doe",
                "birthdate": "2000-01-01",
                "email": "john@example.com",
                "created_at": "2024-01-01",
                "wishlist_id": 1,
            }]
        }
    }

class UserPublic(BaseModel):
    username: str
    created_at: str
    wishlist_id: int

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
        if value >= date.today():
            raise ValueError("Birthdate must be in the past")
        return value


class UserResponseAdd(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str

class UserRequestLogin(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: str

    @model_validator(mode="after")
    def at_least_one_field(self) -> "UserRequestLogin":
        if not any([self.username, self.email]):
            raise ValueError("Необходимо указать либо username, либо email")
        return self


class UserPatch(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None
    birthdate: date | None = None


class WishlistItem(BaseModel):
    game_id: int
    added_at: str
    game: Game

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "game_id": 1,
                "added_at": "2024-01-01",
                "game": Game.model_config["json_schema_extra"]["examples"][0]
            }]
        }
    }


class Wishlist(BaseModel):
    id: int
    user_id: int
    total: int
    items: list[WishlistItem] = []

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "id": 1,
                "user_id": 1,
                "total": 1,
                "items": [WishlistItem.model_config["json_schema_extra"]["examples"][0]]
            }]
        }
    }



