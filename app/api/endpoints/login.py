from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# import crud users
from app import crud
from app.core.security import create_access_token

from app.db.database import getDB
from app.schemas.token import Token
from app.schemas.users import UserInDBBase, Users, UserCreate
from app.api.firebase import auth
from app.crud.crud_users import users as users_crud

router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

@router.post("/signin", response_model=Token)
def login(
    db: Session = Depends(getDB), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.users.authenticate(
        db, email=form_data.username
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email")
    
    # TODO: verify user in firebase
    #elif not crud.users.is_active(user):
    #    raise HTTPException(status_code=400, detail="Inactive user")
    return {
        "access_token": create_access_token(
            user.email, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)),
        "token_type": "bearer",
    }


@router.post("/signup", response_model=Token)
def signup(
    *,
    db: Session = Depends(getDB),
    user_in: UserCreate,
) -> Any:
    """
    Create new user and register to Firebase.
    Returns token auth.
    """
    user = users_crud.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=409,
            detail="The user with this username already exists in the system.",
        )
    user = users_crud.create(db, obj_in=user_in)
    # check if user phone number is already in the system using firebase_admin._auth_utils.PhoneNumberAlreadyExistsError
    auth.create_user(email=user_in.email,
                     phone_number=user_in.phoneNumber)

    return {
        "access_token": create_access_token(
            user.email, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)),
        "token_type": "bearer",
    }
