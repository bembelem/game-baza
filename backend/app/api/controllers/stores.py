from fastapi import APIRouter

from app.api.schemas.stores import Store, StoresResponse

router = APIRouter(prefix="/stores", tags=["Stores"])

@router.get(
    path="/{store_id}",
    response_model=Store
)
def get_stores(store_id: int):
    ...

@router.get(
    path="/",
    response_model=StoresResponse)
def get_store():
    ...


