from typing import Any, Dict, List, Optional, Union

from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.users import Users
from app.schemas.users import UserCreate, UserFollow, UserProfile, UserUpdate


class CRUDUser(CRUDBase[Users, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: EmailStr) -> Optional[Users]:
        return db.query(Users).filter(Users.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> Users:
        db_obj = Users(
            email=obj_in.email,
            firstName=obj_in.firstName,
            lastName=obj_in.lastName,
            phoneNumber=obj_in.phoneNumber,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Users, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> Users:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db, email: str):
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        # if not verify_password(password, user.password):
        #    return None
        return user

    def user_email_prefix(
        self, db: Session, *, emailPrefix: str, limit: int = 100
    ) -> List[UserProfile]:
        return (
            db.query(Users)
            .filter(Users.email.like(emailPrefix + "%"))
            .limit(limit)
            .all()
        )

    def updateUserFollowers(
        self, db: Session, *, db_obj: Users, obj_follower: int
    ) -> UserFollow:
        # add user to user followers
        db_obj.followers.append(obj_follower)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def updateUserFollowing(
        self, db: Session, *, db_obj: Users, obj_following: int
    ) -> UserFollow:
        db_obj.following.append(obj_following)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def deleteUserFromFollower(
        self, db: Session, *, db_obj: Users, obj_follower: int
    ) -> List[UserFollow]:
        # remove user from user's follower list
        db_obj.followers.remove(obj_follower)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def deleteUserFromFollowing(
        self, db: Session, *, db_obj: Users, obj_following: int
    ) -> List[UserFollow]:
        # remove user from user's following list
        db_obj.following.remove(obj_following)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


users = CRUDUser(Users)
