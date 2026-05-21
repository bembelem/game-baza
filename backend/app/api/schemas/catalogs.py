from pydantic import BaseModel

from app.services.schemas.catalogs import (
    Developer,
    Genre,
    Platform,
    Publisher,
    Store,
)


class GenresResponse(BaseModel):
    genres: list[Genre]


class StoresResponse(BaseModel):
    stores: list[Store]


class PlatformsResponse(BaseModel):
    platforms: list[Platform]


class PublishersResponse(BaseModel):
    publishers: list[Publisher]


class DevelopersResponse(BaseModel):
    developers: list[Developer]
