# item.py
from fastapi import APIRouter
from pydantic import BaseModel
import decimal
from datetime import datetime

from . import receivers

router = APIRouter(prefix="/items", tags=["items"])


class Item(BaseModel):
    name: str
    delivery_price: decimal.Decimal = decimal.Decimal("0.0")
    receiver: receivers.Receiver


@router.get(
    "/{item_id}",
    summary="Get an item by ID",
    description="Retrieve an item using its unique identifier.",
)
async def read_item(item_id: int, page: int = 1, size_per_page: int = 50) -> Item:
    return Item(
        name="Sample Item",
        receiver=receivers.Receiver(
            name="Receiver Name",
            email="receiver@example.com",
            id=1,
            created_at=datetime.fromisoformat("2024-01-01T00:00:00+00:00"),
            updated_at=datetime.fromisoformat("2024-01-01T00:00:00+00:00")
        )
    )


@router.get(
    "",
    summary="Get all items",
    description="Retrieve a list of all items.",
)
async def read_items() -> list[Item]:
    return [
        Item(
            name="Item 1",
            receiver=receivers.Receiver(
                name="Receiver 1",
                email="receiver1@example.com",
                id=1,
                created_at=datetime.fromisoformat("2024-01-01T00:00:00+00:00"),
                updated_at=datetime.fromisoformat("2024-01-01T00:00:00+00:00")
            )
        ),
        Item(
            name="Item 2",
            receiver=receivers.Receiver(
                name="Receiver 2",
                email="receiver2@example.com",
                id=2,
                created_at=datetime.fromisoformat("2024-01-02T00:00:00+00:00"),
                updated_at=datetime.fromisoformat("2024-01-02T00:00:00+00:00")
            )
        ),
        Item(
            name="Item 3",
            receiver=receivers.Receiver(
                name="Receiver 3",
                email="receiver3@example.com",
                id=3,
                created_at=datetime.fromisoformat("2024-01-03T00:00:00+00:00"),
                updated_at=datetime.fromisoformat("2024-01-03T00:00:00+00:00")
            )
        ),
    ]


@router.post(
    "",
    summary="Create a new item",
    description="Create a new item with the provided details.",
)
async def create_item(item: Item) -> Item:
    return item


@router.put(
    "/{item_id}",
    summary="Update an existing item",
    description="Update an existing item with the provided details.",
)
async def update_item(item_id: int, item: Item) -> Item:
    return item


@router.delete(
    "/{item_id}",
    summary="Delete an item",
    description="Delete an item using its unique identifier.",
)
async def delete_item(item_id: int) -> dict:
    return {"message": f"Item with id {item_id} deleted successfully."}
