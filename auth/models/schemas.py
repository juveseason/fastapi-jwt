from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


class UserUpdate(UserBase):
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None


class UserDelete(UserBase):
    status: str


class User(UserBase):
    is_active: bool = True
    is_superuser: bool = False


class UserInDB(User):
    id: int
    hashed_password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
