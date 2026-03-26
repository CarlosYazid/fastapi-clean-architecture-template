from typing import Optional

from sqlmodel import Field

from model.abc import BaseModel


class User(BaseModel, table=True):
    email: str = Field(unique=True)
    password: str = Field()

    name: Optional[str] = Field(default=None, nullable=True)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
