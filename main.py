import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.api.api import api_router


# For testing purposes
def create_app():
    _app = FastAPI()

    origins = ["*"]

    _app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    _app.include_router(api_router)

    @_app.get("/", tags=["Home"])
    def home():
        return {"message": "Spotifiuba - 2022"}

    return _app


load_dotenv(".env")
app = create_app()
