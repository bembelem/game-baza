from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel, Field

from backend.app.api.schemas.games import GameFilters


class PaginationParams(BaseModel):
    last_id: int = Field(0, ge=0, description="ID последней записи")
    per_page: int = Field(20, gt=0, le=20, description="Записей на страницу")


PaginationDep = Annotated[PaginationParams, Depends()]
GameFiltersDep = Annotated[GameFilters, Depends()]