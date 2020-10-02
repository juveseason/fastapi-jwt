from sqlalchemy.orm import Session

from auth.controllers import post_user_ctrl
from auth.models.schemas import User, UserCreate
from configuration import settings


def main(db: Session) -> User:
    default_admin_user = UserCreate(
        email=settings.DEFAULT_SUPERUSER_EMAIL,
        full_name=settings.DEFAULT_SUPERUSER_FULL_NAME,
        password=settings.DEFAULT_SUPERUSER_PASSWORD,
        is_active=True,
        is_superuser=True,
    )
    return post_user_ctrl.main(db, default_admin_user)

