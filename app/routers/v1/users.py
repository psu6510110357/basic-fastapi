from uuid import UUID
from fastapi import APIRouter, HTTPException, Query, status, Depends
from sqlmodel import Session, select
import uuid

from app.models.user_model import DBUser as User
from app.core.database import get_session
from app.schemas.user_schemas import (
    CreateUser,
    UpdatedUser,
    UserResponse,
    UserListResponse,
)

router = APIRouter(tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: CreateUser, session: Session = Depends(get_session)):
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

    db_user = User(**user.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return UserResponse(
        id=db_user.id or uuid.uuid4(),  # Generate a valid UUID if id is None
        username=db_user.username,
        email=db_user.email,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
    )


@router.get("/", response_model=UserListResponse)
async def read_users(
    session: Session = Depends(get_session),
    offset: int = Query(default=0),
    limit: int = Query(default=100, le=100),
):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    user_responses = [
        UserResponse(
            id=user.id,  # Assumes user.id is always a UUID
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        for user in users
    ]
    return UserListResponse(users=user_responses)


@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: UUID, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID, user: UpdatedUser, session: Session = Depends(get_session)
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
