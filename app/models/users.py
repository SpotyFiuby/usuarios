from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.dialects.postgresql import BYTEA

from app.db.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firstName = Column(String)
    lastName = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    phoneNumber = Column(String, index=True)
    profileImage = Column(BYTEA, default=b'')
    isPremium = Column(Boolean, nullable=False, default=False)
    isArtist = Column(Boolean, nullable=False, default=False, server_default='False')
