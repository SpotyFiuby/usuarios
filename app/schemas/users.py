import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    phoneNumber: str


class UserInDBBase(UserBase):
    id: int
    dateCreate: datetime.datetime

    class Config:
        orm_mode = True


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


# Additional properties to return via API
class Users(UserInDBBase):
    pass
