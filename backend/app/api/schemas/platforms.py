from pydantic import BaseModel

class Platform(BaseModel):
    id: int
    name: str
    url: str | None = None  # колонки url пока нет в БД, поле зарезервировано

class PlatformsResponse(BaseModel):
    platforms: list[Platform]
