from fastapi import Depends, HTTPException, status, Response
import os
from datetime import timedelta
from jose import JWTError, jwt

from app.schemas.token import TokenPayload

from app.crud.crud_users import users as users_crud
from app.core.security import ALGORITHM, SECRET_KEY, create_access_token, oauth2_scheme

ACCESS_TOKEN_EXPIRE_MINUTES = 1440

def generate_token(db, email):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_access_token(
        data={"sub": email}, expires_delta=access_token_expires
    )


def get_current_user(db, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenPayload(username=username)
    except JWTError:
        raise credentials_exception

    user = users_crud.get_by_email(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
