from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, Query, status, Depends
from sqlmodel import Session, select

from src.models.item import Item
from src.core.database import get_session

router = APIRouter()


@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: Item, session: Session = Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.get("/", response_model=List[Item])
async def read_items(
    session: Session = Depends(get_session),
    offset: int = Query(default=0),
    limit: int = Query(default=100, le=100),
):
    items = session.exec(select(Item).offset(offset).limit(limit)).all()
    return items


@router.get("/{item_id}", response_model=Item)
async def read_item(item_id: UUID, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return item


@router.put("/{item_id}", response_model=Item)
async def update_item(
    item_id: UUID, item: Item, session: Session = Depends(get_session)
):
    db_item = session.get(Item, item_id)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )

    item_data = item.model_dump(exclude_unset=True, exclude={"id"})
    for key, value in item_data.items():
        setattr(db_item, key, value)

    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: UUID, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    session.delete(item)
    session.commit()
    return {"ok": True}
