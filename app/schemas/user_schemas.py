from typing import List
from pydantic import BaseModel, ConfigDict


def to_camel_case(string: str) -> str:
    parts = string.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


class CreateUser(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str  # Added password field

    model_config = ConfigDict(
        validate_by_name=True, alias_generator=to_camel_case, populate_by_name=True
    )


class UpdatedUser(BaseModel):
    username: str | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None

    model_config = ConfigDict(
        validate_by_name=True, alias_generator=to_camel_case, populate_by_name=True
    )


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    first_name: str
    last_name: str

    model_config = ConfigDict(
        validate_by_name=True, populate_by_name=True, alias_generator=to_camel_case
    )


class UserListResponse(BaseModel):
    users: List[UserResponse]


class ReadUsersResponse(BaseModel):
    users: List[UserResponse]
    total_count: int
    has_more: bool
