"""Контроллеры справочников: genres, stores, platforms, publishers, developers."""
from fastapi import APIRouter

from app.api.schemas.catalogs import (
    Developer,
    DevelopersResponse,
    Genre,
    GenresResponse,
    Platform,
    PlatformsResponse,
    Publisher,
    PublishersResponse,
    Store,
    StoresResponse,
)
from app.exceptions import (
    DeveloperNotFoundHTTPException,
    GenreNotFoundHTTPException,
    PlatformNotFoundHTTPException,
    PublisherNotFoundHTTPException,
    StoreNotFoundHTTPException,
)
from app.repositories.catalogs import (
    DeveloperRepository,
    GenreRepository,
    PlatformRepository,
    PublisherRepository,
    StoreRepository,
)
from database.database import async_session_maker


# Genres

router_genres = APIRouter(prefix="/genres", tags=["Genres"])


@router_genres.get("", response_model=GenresResponse, summary="Список жанров")
async def list_genres():
    async with async_session_maker() as session:
        items = await GenreRepository(session).list_all()
    return GenresResponse(genres=[Genre(id=g.id, name=g.name) for g in items])


@router_genres.get(
    "/{genre_id}",
    response_model=Genre,
    summary="Жанр",
    responses={404: {"description": "Жанр не найден"}},
)
async def get_genre(genre_id: int):
    async with async_session_maker() as session:
        item = await GenreRepository(session).get_by_id(genre_id)
    if item is None:
        raise GenreNotFoundHTTPException()
    return Genre(id=item.id, name=item.name)


# Stores

router_stores = APIRouter(prefix="/stores", tags=["Stores"])


@router_stores.get("", response_model=StoresResponse, summary="Список магазинов")
async def list_stores():
    async with async_session_maker() as session:
        items = await StoreRepository(session).list_all()
    return StoresResponse(stores=[Store(id=s.id, name=s.name) for s in items])


@router_stores.get(
    "/{store_id}",
    response_model=Store,
    summary="Магазин",
    responses={404: {"description": "Магазин не найден"}},
)
async def get_store(store_id: int):
    async with async_session_maker() as session:
        item = await StoreRepository(session).get_by_id(store_id)
    if item is None:
        raise StoreNotFoundHTTPException()
    return Store(id=item.id, name=item.name)


# Platforms

router_platforms = APIRouter(prefix="/platforms", tags=["Platforms"])


@router_platforms.get("", response_model=PlatformsResponse, summary="Список платформ")
async def list_platforms():
    async with async_session_maker() as session:
        items = await PlatformRepository(session).list_all()
    return PlatformsResponse(platforms=[Platform(id=p.id, name=p.name) for p in items])


@router_platforms.get(
    "/{platform_id}",
    response_model=Platform,
    summary="Платформа",
    responses={404: {"description": "Платформа не найдена"}},
)
async def get_platform(platform_id: int):
    async with async_session_maker() as session:
        item = await PlatformRepository(session).get_by_id(platform_id)
    if item is None:
        raise PlatformNotFoundHTTPException()
    return Platform(id=item.id, name=item.name)


# Publishers

router_publishers = APIRouter(prefix="/publishers", tags=["Publishers"])


@router_publishers.get("", response_model=PublishersResponse, summary="Список издателей")
async def list_publishers():
    async with async_session_maker() as session:
        items = await PublisherRepository(session).list_all()
    return PublishersResponse(publishers=[Publisher(id=p.id, name=p.name) for p in items])


@router_publishers.get(
    "/{publisher_id}",
    response_model=Publisher,
    summary="Издатель",
    responses={404: {"description": "Издатель не найден"}},
)
async def get_publisher(publisher_id: int):
    async with async_session_maker() as session:
        item = await PublisherRepository(session).get_by_id(publisher_id)
    if item is None:
        raise PublisherNotFoundHTTPException()
    return Publisher(id=item.id, name=item.name)


# Developers

router_developers = APIRouter(prefix="/developers", tags=["Developers"])


@router_developers.get("", response_model=DevelopersResponse, summary="Список разработчиков")
async def list_developers():
    async with async_session_maker() as session:
        items = await DeveloperRepository(session).list_all()
    return DevelopersResponse(developers=[Developer(id=d.id, name=d.name) for d in items])


@router_developers.get(
    "/{developer_id}",
    response_model=Developer,
    summary="Разработчик",
    responses={404: {"description": "Разработчик не найден"}},
)
async def get_developer(developer_id: int):
    async with async_session_maker() as session:
        item = await DeveloperRepository(session).get_by_id(developer_id)
    if item is None:
        raise DeveloperNotFoundHTTPException()
    return Developer(id=item.id, name=item.name)
