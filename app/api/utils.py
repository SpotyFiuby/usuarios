from datetime import timedelta

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from app.core.security import ALGORITHM, SECRET_KEY, create_access_token, oauth2_scheme
from app.crud.crud_users import users as users_crud
from app.schemas.token import TokenPayload

ACCESS_TOKEN_EXPIRE_MINUTES = 1440


def generate_token(email):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_access_token(
        subject={"sub": email}, expires_delta=access_token_expires
    )


def get_current_user(db, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenPayload(email=email)
    except JWTError as e:
        raise credentials_exception from e

    user = users_crud.get_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user
