from dependency_injector.wiring import Provide, inject
from fastapi import Depends
import jwt

from core.container import Container
from core.exceptions import AuthError
from core.security import JWTBearer
from model.user import User
from services.user import UserService
from util.auth import AuthUtils


@inject
async def get_current_user(
    token: str = Depends(JWTBearer()),
    service: UserService = Depends(Provide[Container.user_service]),
) -> User:

    try:
        payload = AuthUtils.decode_jwt(token)

    except jwt.JWTError:
        raise AuthError(detail="Could not validate credentials")

    if not payload.get("id", None):
        raise AuthError(detail="Id not found")

    return await service.read(int(payload["id"]))


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:

    if not current_user.is_active:
        raise AuthError("Inactive user")

    return current_user


def get_current_super_user(
    current_user: User = Depends(get_current_active_user),
) -> User:

    if current_user.is_superuser:
        raise AuthError("It's not a super user")

    return current_user
