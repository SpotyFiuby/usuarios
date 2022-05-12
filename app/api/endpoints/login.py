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

router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

@router.post("/access-token", response_model=Token)
def login_access_token(
    db: Session = Depends(getDB), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.users.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    #elif not crud.users.is_active(user):
    #    raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
