import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = os.environ["DATABASE_URL"]


def fix_dialect(s):
    if s.startswith("postgres://"):
        s = s.replace("postgres://", "postgresql://")
    s = s.replace("postgresql://", "postgresql+psycopg2://")
    return s


engine = create_engine(fix_dialect(SQLALCHEMY_DATABASE_URL))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def getDB() -> Generator:
    try:
        dbSession = SessionLocal()
        yield dbSession
    finally:
        dbSession.close()
