from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, Query, status, Depends
from sqlmodel import Session, select

from src.models.user import User
from src.core.database import get_session

router = APIRouter()


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: User, session: Session = Depends(get_session)):
    existing_user_by_username = session.exec(
        select(User).where(User.username == user.username)
    ).first()
    if existing_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this username already exists",
        )
    existing_user_by_email = session.exec(
        select(User).where(User.email == user.email)
    ).first()
    if existing_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/", response_model=List[User])
async def read_users(
    session: Session = Depends(get_session),
    offset: int = Query(default=0),
    limit: int = Query(default=100, le=100),
):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


@router.get("/{user_id}", response_model=User)
async def read_user(user_id: UUID, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: UUID, user: User, session: Session = Depends(get_session)
):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user_data = user.model_dump(exclude_unset=True, exclude={"id"})
    for key, value in user_data.items():
        setattr(db_user, key, value)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    session.delete(user)
    session.commit()
    return {"ok": True}
