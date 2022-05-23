from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.crud_users import users as users_crud
from app.db.database import getDB
from app.schemas.users import UserProfile, UserProfileModify, Users

router = APIRouter()


@router.get("/", response_model=List[Users])
def readUsers(
    db: Session = Depends(getDB),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve users.
    """
    users = users_crud.get_multi(db, skip=skip, limit=limit)
    if not users:
        raise HTTPException(
            status_code=404,
            detail="There aren't any users.",
        )
    return users


@router.get("/{user_id}", response_model=UserProfile)
def readUserByID(
    user_id: int,
    db: Session = Depends(getDB),
) -> Any:
    """
    Get a specific user by id.
    """
    user = users_crud.get(db, Id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user does not exist in the system",
        )
    return user


@router.put("/{user_id}", response_model=UserProfileModify)
def updateUser(
    *,
    db: Session = Depends(getDB),
    user_id: int,
    user_in: UserProfileModify,
) -> Any:
    """
    Update a user.
    """
    user = users_crud.get(db, Id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user does not exist in the system",
        )
    user = users_crud.update(db, db_obj=user, obj_in=user_in)
    return user


@router.delete("/{user_id}", response_model=Users)
def deleteUser(
    *,
    db: Session = Depends(getDB),
    user_id: int,
) -> Any:
    """
    Delete an user.
    """
    user = users_crud.get(db, Id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = users_crud.remove(db=db, Id=user_id)
    return user


@router.get("/{user_email}", response_model=UserProfile)
def readUserByEmail(
    user_email: int,
    db: Session = Depends(getDB),
) -> Any:
    """
    Get a specific user by email.
    """
    user = users_crud.get_by_email(db, email=user_email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user does not exist in the system",
        )
    return user
