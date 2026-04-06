from pydantic import BaseModel

class Platform(BaseModel):
    id: int
    name: str
    url: str

class PlatformsResponse(BaseModel):
    platforms: list[Platform]
