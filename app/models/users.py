import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import BYTEA

from app.db.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String, index=True)
    lastName = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phoneNumber = Column(String, index=True)
    profileImage = Column(BYTEA)
    isPremium = Column(Boolean, nullable=False, default=False)
    isArtist = Column(Boolean, nullable=False, default=False)
    dateCreate = Column(DateTime, default=datetime.datetime.utcnow)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.datetime.utcnow)
