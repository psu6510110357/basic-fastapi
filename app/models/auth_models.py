from pydantic import BaseModel, EmailStr
import datetime


class Login(BaseModel):
    email: EmailStr
    password: str


class ChangedPassword(BaseModel):
    current_password: str
    new_password: str


class ResetPassword(BaseModel):
    email: EmailStr
    citizen_id: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    expires_at: datetime.datetime
    scope: str
    issued_at: datetime.datetime
    user_id: int
