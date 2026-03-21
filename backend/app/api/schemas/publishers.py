from pydantic import BaseModel

class Publisher(BaseModel):
    id: int
    name: str

class PublishersResponse(BaseModel):
    publishers: list[Publisher]
