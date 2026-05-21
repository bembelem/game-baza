from datetime import date

from pydantic import BaseModel


class UserPatch(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None
    birthdate: date | None = None