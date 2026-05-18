from pydantic import BaseModel

class Store(BaseModel):
    id: int
    name: str
    url: str | None = None  # колонки url пока нет в БД, поле зарезервировано

class StoresResponse(BaseModel):
    stores: list[Store]
