from datetime import timedelta
import json
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
import requests
from sqlalchemy.orm import Session

# import crud users
from app import crud
from app.core.security import create_access_token

from app.db.database import getDB
from app.schemas.token import Token
from app.schemas.users import UserInDBBase, Users, UserCreate, UserSignIn
from app.api.firebase import auth, FIREBASE_WEB_API_KEY
from app.crud.crud_users import users as users_crud

router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = 1440


def sign_in_with_email_and_password(email, password, return_secure_token=True):
    payload = json.dumps({"email": email,
                          "password": password,
                          "return_secure_token": return_secure_token})
    rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

    r = requests.post(rest_api_url,
                      params={"key": FIREBASE_WEB_API_KEY},
                      data=payload)

    return r.json()


@router.post("/signin", response_model=Any)
def login(
    db: Session = Depends(getDB), form_data: UserSignIn = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    try:
        firebase_user = sign_in_with_email_and_password(form_data.email,
                                                        form_data.password,
                                                        return_secure_token=True)
    except Exception:
        return HTTPException(status_code=400, detail="User not found.")

    user = crud.users.authenticate(
        db, email=form_data.email
    )
    if not user:
        print("User not found in DB: {}".format(form_data.email))
        raise HTTPException(status_code=400, detail="Incorrect email")

    uid = firebase_user['localId']
    token = auth.create_custom_token(uid)
    return {"token": token}


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
            status_code=401,
            detail="The user with this username already exists in the system.",
        )
    user = users_crud.create(db, obj_in=user_in)
    try:
        auth.create_user(email=user_in.email,
                         phone_number=user_in.phoneNumber)
    except Exception:
        return HTTPException(status_code=401, detail="User already exists.")

    return {
        "access_token": create_access_token(
            user.email, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)),
        "token_type": "bearer",
    }