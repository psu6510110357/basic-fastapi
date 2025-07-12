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
    email: str | None = Field(
        None, json_schema_extra={"example": "updated@email.local"}
    )
    username: str | None = Field(
        None, json_schema_extra={"example": "updated_username"}
    )
    first_name: str | None = Field(
        None, json_schema_extra={"example": "UpdatedFirstname"}
    )
    last_name: str | None = Field(
        None, json_schema_extra={"example": "UpdatedLastname"}
    )
    password: str | None = Field(
        None, json_schema_extra={"example": "updated_password"}
    )


class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str


class UserListResponse(BaseModel):
    users: List[UserResponse]
