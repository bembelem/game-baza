from datetime import date

from pydantic import BaseModel, EmailStr, Field

from app.services.schemas.games import GameCard


class UserPrivate(BaseModel):
    """Полный профиль пользователя — отдаём только владельцу (/users/me)."""
    id: int
    email: EmailStr
    birthdate: date
    username: str
    created_at: date


class UserPublic(BaseModel):
    """Публичный профиль — только безопасные поля, отдаём наружу."""
    username: str
    created_at: str


class WishlistItem(BaseModel):
    """Одна игра в вишлисте с датой добавления."""
    game: GameCard
    added_at: str


class Wishlist(BaseModel):
    """Вишлист пользователя целиком — список WishlistItem + метаданные."""
    id: int
    user_id: int
    total: int
    items: list[WishlistItem] = []
