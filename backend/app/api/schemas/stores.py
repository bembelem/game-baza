from pydantic import BaseModel

class Store(BaseModel):
    id: int
    name: str
    url: str

class StoresResponse(BaseModel):
    stores: list[Store]
