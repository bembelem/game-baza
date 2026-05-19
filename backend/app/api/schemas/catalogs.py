"""Схемы справочников: genres, stores, platforms, publishers, developers."""
from pydantic import BaseModel


# Genres

class Genre(BaseModel):
    id: int
    name: str


class GenresResponse(BaseModel):
    genres: list[Genre]


# Stores

class Store(BaseModel):
    id: int
    name: str
    url: str | None = None  # колонки url пока нет в БД, поле зарезервировано


class StoresResponse(BaseModel):
    stores: list[Store]


# Platforms

class Platform(BaseModel):
    id: int
    name: str
    url: str | None = None  # колонки url пока нет в БД, поле зарезервировано


class PlatformsResponse(BaseModel):
    platforms: list[Platform]


# Publishers

class Publisher(BaseModel):
    id: int
    name: str


class PublishersResponse(BaseModel):
    publishers: list[Publisher]


# Developers

class Developer(BaseModel):
    id: int
    name: str


class DevelopersResponse(BaseModel):
    developers: list[Developer]
