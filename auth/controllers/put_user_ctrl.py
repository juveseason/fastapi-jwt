from fastapi import HTTPException
from sqlalchemy.orm import Session

from auth.controllers.get_user_ctrl import (create_user_from_db,
                                            get_db_user_by_email)
from auth.controllers.post_token_ctrl import get_password_hash
from auth.models.schemas import User, UserUpdate


def main(db: Session, user: UserUpdate) -> User:
    db_user = get_db_user_by_email(db, user.email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.full_name is not None:
        db_user.full_name = user.full_name
    if user.password is not None:
        db_user.hashed_password = get_password_hash(user.password)
    if user.is_active is not None:
        db_user.is_active = user.is_active
    if user.is_superuser is not None:
        db_user.is_superuser = user.is_superuser
    db.commit()
    db.refresh(db_user)
    updated_user = create_user_from_db(db_user)
    return updated_user
