from pydantic import BaseModel

class Genre(BaseModel):
    id: int
    title: str

class GenresResponse(BaseModel):
    genres: list[Genre]