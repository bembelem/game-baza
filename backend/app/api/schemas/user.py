from pydantic import BaseModel
from backend.app.api.v1.schemas.games import GamePreview

class CommentDTO(BaseModel):
    id: int
    game_id: int
    text: str
    created_at: str

class WishlistItemDTO(BaseModel):
    game_id: int
    added_at: str
    game: GamePreview

class WishlistDTO(BaseModel):
    total: int
    items: list[WishlistItemDTO] = []

class UserDTO(BaseModel):
    id: int
    username: str
    email: str
    created_at: str
    wishlist_count: int = 0
    comments_count: int = 0