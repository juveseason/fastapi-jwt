from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy.orm import Session
from utils.database import get_db
from auth.controllers import (
    delete_user_ctrl,
    get_user_ctrl,
    get_users_all_ctrl,
    post_default_superuser_ctrl,
    post_token_ctrl,
    post_user_ctrl,
    put_user_ctrl,
)
from auth.controllers.post_token_ctrl import (
    get_current_active_superuser,
    get_current_active_user,
)
from auth.models.schemas import Token, User, UserCreate, UserDelete, UserUpdate


router = APIRouter()


@router.post("/users/init", response_model=User)
def post_default_superuser(db: Session = Depends(get_db)) -> User:
    """
    Create the default superuser. Run this once when deploy a new app.
    """
    return post_default_superuser_ctrl.main(db)


@router.post("/token", response_model=Token)
def post_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> Token:
    """
    OAuth2 login, return access token.
    """
    return post_token_ctrl.main(db, form_data)


@router.get("/users/me", response_model=User)
def get_users_me(current_user: User = Depends(get_current_active_user)) -> User:
    """
    Get current user details.
    """
    return current_user


@router.get("/users", response_model=User)
def get_user(
    email: EmailStr,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> User:
    """
    Get user detials by email.
    Require superuser privilege
    """
    return get_user_ctrl.main(db, email)


@router.post("/users", response_model=User)
def post_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> User:
    """
    Create new user.
    Require superuser privilege
    """
    return post_user_ctrl.main(db, user)


@router.put("/users", response_model=User)
def put_user(
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> User:
    """
    Update user details (full_name, password, is_active, is_superuser) by email.
    Require superuser privilege
    """
    return put_user_ctrl.main(db, user)


@router.delete("/users", response_model=UserDelete)
def delete_user(
    email: EmailStr,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> UserDelete:
    """
    Delete user by email.
    Require superuser privilege
    """
    return delete_user_ctrl.main(db, email)


@router.get("/users/all", response_model=List[User])
def get_users_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> List[User]:
    """
    Get all users details.
    Require superuser privilege
    """
    return get_users_all_ctrl.main(db)
