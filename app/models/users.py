import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.db.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firstName = Column(String)
    lastName = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    phoneNumber = Column(String, index=True)
    dateCreated = Column(DateTime, default=datetime.datetime.utcnow)
    dateUpdated = Column(DateTime(timezone=True), onupdate=datetime.datetime.utcnow)
