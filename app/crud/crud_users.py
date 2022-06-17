from typing import Any, Dict, List, Optional, Union

from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.users import Users
from app.schemas.users import UserCreate, UserUpdate


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
    ) -> List[Users]:
        return (
            db.query(Users)
            .filter(Users.email.like(emailPrefix + "%"))
            .limit(limit)
            .all()
        )


users = CRUDUser(Users)
