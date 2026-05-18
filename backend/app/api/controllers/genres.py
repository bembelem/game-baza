from fastapi import APIRouter

from app.api.schemas.genres import Genre, GenresResponse
from app.exceptions import GenreNotFoundHTTPException
from app.repositories.catalogs import GenreRepository
from database.database import async_session_maker

router = APIRouter(prefix="/genres", tags=["Genres"])


@router.get(
    "",
    response_model=GenresResponse,
    summary="Список жанров",
    description="Возвращает список всех жанров игр.",
)
async def list_genres():
    async with async_session_maker() as session:
        items = await GenreRepository(session).list_all()
    return GenresResponse(genres=[Genre(id=g.id, name=g.name) for g in items])


@router.get(
    "/{genre_id}",
    response_model=Genre,
    summary="Жанр",
    description="Возвращает информацию о жанре по его ID.",
    responses={404: {"description": "Жанр не найден"}},
)
async def get_genre(genre_id: int):
    async with async_session_maker() as session:
        genre = await GenreRepository(session).get_by_id(genre_id)
    if genre is None:
        raise GenreNotFoundHTTPException()
    return Genre(id=genre.id, name=genre.name)
