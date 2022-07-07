from sqlalchemy import ARRAY, Boolean, Column, Integer, String

from app.db.database import Base
from app.models.sqlal_mutable_array import MutableList


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firstName = Column(String)
    lastName = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    phoneNumber = Column(String, index=True)
    profileImage = Column(
        String,
        default="https://cdn0.iconfinder.com/data/icons/body-parts-glyph-silhouettes/300/161845119Untitled-3-512.png",
    )
    isPremium = Column(Boolean, nullable=False, default=False)
    isArtist = Column(Boolean, nullable=False, default=False, server_default='False')
    username = Column(String)
    location = Column(String)
    biography: str = Column(String)
    following = Column(MutableList.as_mutable(ARRAY(Integer())), default=[])
    followers = Column(MutableList.as_mutable(ARRAY(Integer())), default=[])
    privateKey = Column(String, default='')
    publicKey = Column(String, default='')
    address = Column(String, default='')
    transactionHash = Column(String, default='')
    tokenNotification = Column(String, default='')
