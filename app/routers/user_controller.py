from fastapi import APIRouter
from .user import User, UserStatus, UserRequest, UserWithoutId
from .helper import Message
from fastapi.responses import JSONResponse
import random
from datetime import datetime
import json
from fastapi.encoders import jsonable_encoder
import os

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get('/',description="Fetch all users")
async def get_all_users():
    return []

@router.get('/{user_id}', description="Fetch a single user by Id", response_model=User, responses={404: {"model": Message}})
async def get_user_by_id(user_id: int):
    return []
    # In case of error:
    # return JSONResponse(status_code=404, content={"message": "The user doesn't exist"})

@router.post("/", description="Create a new user", responses={404: {"model": Message}})
async def create_user(user_request: UserRequest):
    try:
        # Create the Id (if necessary) and save in the object User like this:
        # User(**user_request.dict(), id = id)
        return id
    except:
        return JSONResponse(status_code=404, content={"message": "Error when creating new user"})

@router.put("/{user_id}", description="Update user by Id", responses={404: {"model": Message}})
def update_user(user_id: int, new_user: UserWithoutId):
    # Save in the object User like this:
    # User(**new_user.dict(), id = user_id) 
    return JSONResponse(status_code=404, content={"message": "The user doesn't exist. You should create it before modifying."})

@router.delete("/{user_id}", description="Delete user by Id", responses={404: {"model": Message}})
def delete_user(user_id: int):
    return "The user could be deleted successfully"
    return JSONResponse(status_code=404, content={"message": "No existe el user que se desea eliminar"})
