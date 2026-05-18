from fastapi import APIRouter

from app.api.schemas.platforms import Platform, PlatformsResponse
from app.exceptions import PlatformNotFoundHTTPException
from app.repositories.catalogs import PlatformRepository
from database.database import async_session_maker

# в openapi контракт /platforms, но в коде исторически было /platform —
# оставляю /platforms (см. правки openapi.yaml).
router = APIRouter(prefix="/platforms", tags=["Platforms"])


@router.get(
    "",
    response_model=PlatformsResponse,
    summary="Список платформ",
    description="Возвращает список всех игровых платформ.",
)
async def list_platforms():
    async with async_session_maker() as session:
        items = await PlatformRepository(session).list_all()
    return PlatformsResponse(platforms=[Platform(id=p.id, name=p.name) for p in items])


@router.get(
    "/{platform_id}",
    response_model=Platform,
    summary="Платформа",
    description="Возвращает платформу по её ID.",
    responses={404: {"description": "Платформа не найдена"}},
)
async def get_platform(platform_id: int):
    async with async_session_maker() as session:
        platform = await PlatformRepository(session).get_by_id(platform_id)
    if platform is None:
        raise PlatformNotFoundHTTPException()
    return Platform(id=platform.id, name=platform.name)
