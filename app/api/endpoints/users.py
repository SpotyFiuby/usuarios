from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.crud_users import users as users_crud

# import getDB from app/db/database.py
from app.db.database import getDB
from app.schemas.users import Users

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
            status_code=400,
            detail="Error getting all the users.",
        )
    return users


@router.post("/", response_model=Users)
def createUser(
    *,
    db: Session = Depends(getDB),
    user_in: Users,
) -> Any:
    """
    Create new user.
    """
    user = users_crud.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = users_crud.create(db, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=Users)
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


@router.put("/{user_id}", response_model=Users)
def updateUser(
    *,
    db: Session = Depends(getDB),
    user_id: int,
    user_in: Users,
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
    Delete an item.
    """
    user = users_crud.get(db, Id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Item not found")
    user = users_crud.remove(db=db, Id=user_id)
    return user
