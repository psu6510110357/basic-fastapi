from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):

    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    full_name: Optional[str] = None

    json_schema_extra = {
        "example": {
            "username": "johndoe",
            "email": "john.doe@example.com",
            "full_name": "John Doe",
        }
    }
