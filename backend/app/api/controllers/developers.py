from fastapi import APIRouter

from app.api.schemas.developers import Developer, DevelopersResponse
from app.exceptions import DeveloperNotFoundHTTPException
from app.repositories.catalogs import DeveloperRepository
from database.database import async_session_maker

router = APIRouter(prefix="/developers", tags=["Developers"])


@router.get(
    "",
    response_model=DevelopersResponse,
    summary="Список разработчиков",
    description="Возвращает список всех разработчиков.",
)
async def list_developers():
    async with async_session_maker() as session:
        items = await DeveloperRepository(session).list_all()
    return DevelopersResponse(developers=[Developer(id=d.id, name=d.name) for d in items])


@router.get(
    "/{developer_id}",
    response_model=Developer,
    summary="Разработчик",
    description="Возвращает разработчика по его ID.",
    responses={404: {"description": "Разработчик не найден"}},
)
async def get_developer(developer_id: int):
    async with async_session_maker() as session:
        dev = await DeveloperRepository(session).get_by_id(developer_id)
    if dev is None:
        raise DeveloperNotFoundHTTPException()
    return Developer(id=dev.id, name=dev.name)
