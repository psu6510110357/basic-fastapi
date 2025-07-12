from typing import List
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str

class UserListResponse(BaseModel):
    users: List[UserResponse]
