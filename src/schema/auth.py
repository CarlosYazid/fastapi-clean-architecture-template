from datetime import datetime

from pydantic import BaseModel

from src.schema.user import UserRead


class SignBase(BaseModel):
    email: str
    password: str


class SignIn(SignBase):
    pass


class SignUp(SignBase):
    name: str


class SignInResponse(BaseModel):
    access_token: str
    expiration: datetime
    user_info: UserRead
