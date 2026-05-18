from pydantic import BaseModel


class Developer(BaseModel):
    id: int
    name: str


class DevelopersResponse(BaseModel):
    developers: list[Developer]
