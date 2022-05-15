import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class CustomBaseModel(BaseModel):
    class Config:
        orm_mode = True


# Shared properties
class UserBase(CustomBaseModel):
    firstName: str
    lastName: str


class UserBaseComplete(UserBase):
    email: EmailStr
    phoneNumber: str


class UserInDBBase(UserBaseComplete):
    id: int
    dateCreate: datetime.datetime


# Properties to receive via API on creation
class UserCreate(UserBaseComplete):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBaseComplete):
    password: Optional[str] = None


# Additional properties to return via API
class Users(UserInDBBase):
    pass


class UserProfile(UserBaseComplete):
    isPremium: bool = False
    isArtist: bool = False
    profileImage: bytes = b''


class UserProfileModify(UserBase):
    isArtist: bool = False
    profileImage: bytes = b''
