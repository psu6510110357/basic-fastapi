import datetime
from uuid import UUID
import uuid

import pydantic
from pydantic import BaseModel, ConfigDict
from sqlmodel import SQLModel, Field

import bcrypt


class BaseUser(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    email: str = pydantic.Field(json_schema_extra=dict(example="admin@email.local"))
    username: str = pydantic.Field(json_schema_extra=dict(example="admin"))
    first_name: str = pydantic.Field(json_schema_extra=dict(example="Firstname"))
    last_name: str = pydantic.Field(json_schema_extra=dict(example="Lastname"))
    status: str = pydantic.Field(json_schema_extra=dict(example="active"))


class User(BaseUser):
    id: UUID
    last_login_date: datetime.datetime | None = pydantic.Field(
        json_schema_extra=dict(example="2023-01-01T00:00:00.000000"), default=None
    )
    register_date: datetime.datetime | None = pydantic.Field(
        json_schema_extra=dict(example="2023-01-01T00:00:00.000000"), default=None
    )


class DBUser(BaseUser, SQLModel, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    password: str

    register_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    last_login_date: datetime.datetime | None = Field(default=None)
    status: str = Field(default="active")

    async def get_encrypted_password(self, plain_password):
        return bcrypt.hashpw(
            plain_password.encode("utf-8"), salt=bcrypt.gensalt()
        ).decode("utf-8")

    async def set_password(self, plain_password):
        self.password = await self.get_encrypted_password(plain_password)

    async def verify_password(self, plain_password):
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), self.password.encode("utf-8")
        )


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    expires_at: datetime.datetime
    scope: str
    issued_at: datetime.datetime
    user_id: UUID
