from pydantic import BaseModel


class Genre(BaseModel):
    id: int
    name: str


class Store(BaseModel):
    id: int
    name: str
    url: str | None = None  # колонки url пока нет в БД, поле зарезервировано


class Platform(BaseModel):
    id: int
    name: str
    url: str | None = None  # колонки url пока нет в БД, поле зарезервировано


class Publisher(BaseModel):
    id: int
    name: str


class Developer(BaseModel):
    id: int
    name: str
