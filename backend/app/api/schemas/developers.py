from pydantic import BaseModel

class Developer(BaseModel):
    id: int
    name: str