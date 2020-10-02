from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from auth.controllers.get_user_ctrl import create_user_from_db
from auth.models.schemas import User, UserInDB
from auth.models.user import UserTable


def main(db: Session) -> List[User]:
    db_users = get_db_users_all(db)
    if db_users is None:
        raise HTTPException(status_code=404, detail="User not found")
    user = create_users_from_db(db_users)
    return user


def get_db_users_all(db: Session) -> List[UserInDB]:
    return db.query(UserTable).all()


def create_users_from_db(db_users: List[UserInDB]) -> List[User]:
    users = []
    for db_user in db_users:
        user = create_user_from_db(db_user)
        users.append(user)
    return users
