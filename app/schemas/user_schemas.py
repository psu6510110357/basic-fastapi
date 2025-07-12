from typing import List
from pydantic import BaseModel, Field
import uuid


class CreateUser(BaseModel):
    email: str = Field(..., json_schema_extra={"example": "admin@email.local"})
    username: str = Field(..., json_schema_extra={"example": "admin"})
    first_name: str = Field(..., json_schema_extra={"example": "Firstname"})
    last_name: str = Field(..., json_schema_extra={"example": "Lastname"})
    password: str = Field(..., json_schema_extra={"example": "password"})


class UpdatedUser(BaseModel):
    roles: list[str]


class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str


class UserListResponse(BaseModel):
    users: List[UserResponse]
