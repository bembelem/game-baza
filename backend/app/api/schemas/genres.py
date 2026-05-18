from pydantic import BaseModel

class Genre(BaseModel):
    id: int
    name: str

class GenresResponse(BaseModel):
    genres: list[Genre]