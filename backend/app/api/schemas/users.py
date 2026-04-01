from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator, model_validator

from backend.app.api.schemas.games import Game


# Базовая модель пользователя — используется как основа или для внутренних нужд
class User(BaseModel):
    id: int
    email: EmailStr
    birthdate: date
    username: str
    created_at: date

# Публичный профиль — только безопасные поля, отдаём наружу
class UserPublic(BaseModel):
    username: str
    created_at: str

# Частичное обновление профиля — все поля опциональны (PATCH)
class UserPatch(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None
    birthdate: date | None = None


# Одна игра в вишлисте с датой добавления
class WishlistItem(BaseModel):
    game: Game
    added_at: str

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "game_id": 1,
                "added_at": "2024-01-01",
                "game": Game.model_config["json_schema_extra"]["examples"][0]  # type: ignore
            }]
        }
    }


# Вишлист пользователя целиком — список WishlistItem + метаданные
class Wishlist(BaseModel):
    id: int
    user_id: int
    total: int  # общее количество игр
    items: list[WishlistItem] = []

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "id": 1,
                "user_id": 1,
                "total": 1,
                "items": [WishlistItem.model_config["json_schema_extra"]["examples"][0]]  # type: ignore
            }]
        }
    }