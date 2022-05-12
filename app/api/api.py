from fastapi import APIRouter

from app.api.endpoints import users
from app.api.endpoints import login

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(login.router, prefix="/login", tags=["login"])
