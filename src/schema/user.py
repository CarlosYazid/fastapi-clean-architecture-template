from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    id: int


class UserRead(UserBase):
    email: str
    name: Optional[str]
    is_superuser: bool


class UserUpdate(UserBase):
    name: Optional[str]
    is_superuser: Optional[bool]


class UserCreate(BaseModel):
    email: str
    name: Optional[str]
    is_superuser: bool
