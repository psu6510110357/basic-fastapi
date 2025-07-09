from typing import ClassVar, Optional
from uuid import UUID, uuid4
from pydantic import ConfigDict
from sqlmodel import Field, SQLModel


class Item(SQLModel, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

    json_schema_extra: ClassVar[dict] = {
        "example": {
            "name": "Super Widget",
            "description": "A very useful widget.",
            "price": 29.99,
            "tax": 3.00,
        }
    }
