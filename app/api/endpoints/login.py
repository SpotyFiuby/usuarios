from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api.firebase import auth
from app.api.utils import sign_in_with_email_and_password
from app.crud.crud_users import users as users_crud
from app.db.database import getDB
from app.schemas.users import UserCreate, UserSignIn

router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = 1440


@router.post("/signin", response_model=Any)
def login(*, db: Session = Depends(getDB), form_data: UserSignIn) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    firebase_user = sign_in_with_email_and_password(
        form_data.email, form_data.password, return_secure_token=True
    )
    if "error" in firebase_user:
        raise HTTPException(status_code=400, detail="Incorrect email/password.")

    user = crud.users.authenticate(db, email=form_data.email)
    if not user:
        print("User not found in DB: {}".format(form_data.email))
        raise HTTPException(status_code=400, detail="Incorrect email")

    firebase_token = auth.create_custom_token(firebase_user["localId"])
    return {"token": firebase_token}


@router.post("/signup", response_model=Any)
def signup(
    *,
    db: Session = Depends(getDB),
    user_in: UserCreate,
) -> Any:
    """
    Create new user and register to Firebase.
    Returns token auth.
    """
    try:
        firebase_user = auth.create_user(email=user_in.email, password=user_in.password)
    except Exception as e:
        raise HTTPException(status_code=401, detail="User already exists.") from e

    user = users_crud.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=401,
            detail="The user with this username already exists in the system.",
        )
    user = users_crud.create(db, obj_in=user_in)

    firebase_token = auth.create_custom_token(firebase_user.uid)
    return {"token": firebase_token}
