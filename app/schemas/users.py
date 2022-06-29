from typing import List, Optional

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


# Properties to receive via API on creation
class UserCreate(UserBaseComplete):
    email: EmailStr
    password: str


class UserSignIn(BaseModel):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBaseComplete):
    pass


# Additional properties to return via API
class Users(UserInDBBase):
    pass


class UserProfile(UserBaseComplete):
    isPremium: bool = False
    isArtist: bool = False
    profileImage: Optional[str] = ''
    username: Optional[str] = ''
    location: Optional[str] = ''
    biography: Optional[str] = ''
    id: int
    following: List[int] = []
    followers: List[int] = []


class UserProfileModify(UserBase):
    isArtist: bool = False
    profileImage: Optional[str] = ''
    username: Optional[str] = ''
    location: Optional[str] = ''
    biography: Optional[str] = ''


class UserFollow(UserProfile):
    following: List[int] = []
    followers: List[int] = []
