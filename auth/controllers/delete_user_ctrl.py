from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session

from auth.controllers.get_user_ctrl import get_db_user_by_email
from auth.models.schemas import UserDelete


def main(db: Session, email: EmailStr) -> UserDelete:
    db_user = get_db_user_by_email(db, email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    deleted_user = UserDelete(
        email=db_user.email, full_name=db_user.full_name, status="deleted"
    )
    return deleted_user

