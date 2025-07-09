from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class ReceiverBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    is_active: bool = True


class ReceiverCreate(ReceiverBase):
    pass


class ReceiverUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None


class Receiver(ReceiverBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
