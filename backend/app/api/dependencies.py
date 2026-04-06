from typing import Annotated

from fastapi import Depends, Request
from pydantic import BaseModel, Field

from app.api.schemas.games import GameFilters
from app.exceptions import IncorrectTokenHTTPException
from app.services.auth import AuthService


class PaginationParams(BaseModel):
    last_id: int = Field(0, ge=0, description="ID последней записи")
    per_page: int = Field(20, gt=0, le=20, description="Записей на страницу")


PaginationDep = Annotated[PaginationParams, Depends()]
GameFiltersDep = Annotated[GameFilters, Depends()]

def get_token(request: Request):
    access_token = request.cookies.get("access_token", None)
    if access_token is None:
        raise IncorrectTokenHTTPException()
    return access_token

def get_user_id(access_token: str = Depends(get_token)) -> int:
    data = AuthService().decode_token(access_token)
    user_id = data["user_id"]
    return user_id

UserIdDep = Annotated[int, Depends(get_user_id)]
