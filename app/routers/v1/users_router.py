from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, HTTPException, Query, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, func
import uuid

from app.models.user_model import DBUser as User
from app.core.database import get_session
from app.schemas.user_schemas import (
    CreateUser,
    ReadUsersResponse,
    UpdatedUser,
    UserResponse,
)

router = APIRouter(tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: CreateUser,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UserResponse:
    # Check if username already exists
    result = await session.exec(select(User).where(User.username == user.username))
    existing_user_by_username = result.first()
    if existing_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this username already exists",
        )

    # Check if email already exists
    result = await session.exec(select(User).where(User.email == user.email))
    existing_user_by_email = result.first()
    if existing_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    # Hash the password before storing
    hashed_password = await User(
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        password="",
    ).get_encrypted_password(user.password)

    db_user = User(
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        password=hashed_password,  # Store hashed password
        id=uuid.uuid4(),  # Generate UUID
    )

    # Save user to the database
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    # Return the created user
    return UserResponse(
        id=str(db_user.id),
        username=db_user.username,
        email=db_user.email,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
    )


@router.get("/", response_model=ReadUsersResponse)
async def read_users(
    session: Annotated[AsyncSession, Depends(get_session)],
    offset: int = Query(default=0),
    limit: int = Query(default=100, le=100),
) -> ReadUsersResponse:
    total_count_result = await session.exec(select(func.count()).select_from(User))
    total_count = total_count_result.one()

    result = await session.exec(select(User).offset(offset).limit(limit))
    users = result.all()
    user_responses = [
        UserResponse(
            id=str(user.id),
            username=user.username,
            email=user.email,
            first_name=user.first_name,  # Use snake_case for initialization
            last_name=user.last_name,  # Use snake_case for initialization
        )
        for user in users
    ]

    has_more = offset + limit < total_count

    return ReadUsersResponse(
        users=user_responses,
        total_count=total_count,
        has_more=has_more,
    )


@router.get("/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: UUID, session: Annotated[AsyncSession, Depends(get_session)]
) -> UserResponse:
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return UserResponse(
        id=str(user.id),
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
    )


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    user: UpdatedUser,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UserResponse:
    db_user = await session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user_data = user.model_dump(exclude_unset=True, exclude={"id"})
    for key, value in user_data.items():
        setattr(db_user, key, value)

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return UserResponse(
        id=(str(db_user.id)),
        username=db_user.username,
        email=db_user.email,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID, session: Annotated[AsyncSession, Depends(get_session)]
) -> None:
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    await session.delete(user)
    await session.commit()
