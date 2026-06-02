from typing import Optional

from pydantic import BaseModel, EmailStr, model_validator, ConfigDict

from app.api.schemas.auth import UsernameStr, PasswordStr, BirthDate


def _empty_str_to_none(value):
    if isinstance(value, str) and value.strip() == "":
        return None
    return value

class UserPatch(BaseModel):
    username: Optional[UsernameStr] = None
    password: Optional[PasswordStr] = None
    birthdate: Optional[BirthDate] = None

    model_config = ConfigDict(regex_engine="python-re")

    @model_validator(mode="before")
    @classmethod
    def convert_empty_strings(cls, data: dict) -> dict:
        return {k: _empty_str_to_none(v) for k, v in data.items()}