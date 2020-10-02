from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session

from auth.models.schemas import User, UserInDB
from auth.models.user import UserTable


def main(db: Session, email: EmailStr) -> User:
    db_user = get_db_user_by_email(db, email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user = create_user_from_db(db_user)
    return user


def get_db_user_by_email(db: Session, email: EmailStr) -> UserInDB:
    return db.query(UserTable).filter(UserTable.email == email).first()


def create_user_from_db(db_user: UserInDB) -> User:
    user = User(
        email=db_user.email,
        full_name=db_user.full_name,
        is_active=db_user.is_active,
        is_superuser=db_user.is_superuser,
    )
    return user
