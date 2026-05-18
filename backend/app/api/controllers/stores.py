from fastapi import APIRouter

from app.api.schemas.stores import Store, StoresResponse
from app.exceptions import StoreNotFoundHTTPException
from app.repositories.catalogs import StoreRepository
from database.database import async_session_maker

router = APIRouter(prefix="/stores", tags=["Stores"])


@router.get(
    "",
    response_model=StoresResponse,
    summary="Список магазинов",
    description="Возвращает список всех магазинов.",
)
async def list_stores():
    async with async_session_maker() as session:
        items = await StoreRepository(session).list_all()
    return StoresResponse(stores=[Store(id=s.id, name=s.name) for s in items])


@router.get(
    "/{store_id}",
    response_model=Store,
    summary="Магазин",
    description="Возвращает магазин по его ID.",
    responses={404: {"description": "Магазин не найден"}},
)
async def get_store(store_id: int):
    async with async_session_maker() as session:
        store = await StoreRepository(session).get_by_id(store_id)
    if store is None:
        raise StoreNotFoundHTTPException()
    return Store(id=store.id, name=store.name)
