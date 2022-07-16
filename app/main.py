import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.api.api import api_router
from app.logger import create_logger

logger = create_logger()


def fix_dialect(s):
    if s.startswith("postgres://"):
        s = s.replace("postgres://", "postgresql://")
    s = s.replace("postgresql://", "postgresql+psycopg2://")
    return s


# For testing purposes
def create_app():
    _app = FastAPI()

    origins = ["*"]

    db_url = fix_dialect(os.environ["DATABASE_URL"])

    _app.add_middleware(DBSessionMiddleware, db_url=db_url)
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
        logger.info("Starting application...")
        return {"message": "Spotifiuba - 2022"}

    return _app


load_dotenv(".env")
app = create_app()
