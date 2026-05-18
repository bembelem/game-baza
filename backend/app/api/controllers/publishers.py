from fastapi import APIRouter

from app.api.schemas.publishers import Publisher, PublishersResponse
from app.exceptions import PublisherNotFoundHTTPException
from app.repositories.catalogs import PublisherRepository
from database.database import async_session_maker

router = APIRouter(prefix="/publishers", tags=["Publishers"])


@router.get(
    "",
    response_model=PublishersResponse,
    summary="Список издателей",
    description="Возвращает список всех издателей.",
)
async def list_publishers():
    async with async_session_maker() as session:
        items = await PublisherRepository(session).list_all()
    return PublishersResponse(publishers=[Publisher(id=p.id, name=p.name) for p in items])


@router.get(
    "/{publisher_id}",
    response_model=Publisher,
    summary="Издатель",
    description="Возвращает издателя по его ID.",
    responses={404: {"description": "Издатель не найден"}},
)
async def get_publisher(publisher_id: int):
    async with async_session_maker() as session:
        pub = await PublisherRepository(session).get_by_id(publisher_id)
    if pub is None:
        raise PublisherNotFoundHTTPException()
    return Publisher(id=pub.id, name=pub.name)
