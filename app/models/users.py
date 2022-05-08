import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.db.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String, index=True)
    lastName = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phoneNumber = Column(String, index=True)
    dateCreate = Column(DateTime, default=datetime.datetime.utcnow)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.datetime.utcnow)
