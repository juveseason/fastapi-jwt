from fastapi import HTTPException
from sqlalchemy.orm import Session

from auth.controllers.get_user_ctrl import (create_user_from_db,
                                            get_db_user_by_email)
from auth.controllers.post_token_ctrl import get_password_hash
from auth.models.schemas import User, UserCreate
from auth.models.user import UserTable


def main(db: Session, user: UserCreate) -> User:
    db_user = get_db_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)


def create_user(db: Session, user: UserCreate) -> User:
    db_user = UserTable(
        email=user.email,
        full_name=user.full_name,
        hashed_password=get_password_hash(user.password),
        is_active=user.is_active,
        is_superuser=user.is_superuser,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    user = create_user_from_db(db_user)
    return user
