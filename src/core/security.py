from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.util.auth import AuthUtils
from src.core.exceptions import AuthError


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):

        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise AuthError(detail="Invalid authentication scheme.")

            if not AuthUtils.verify_jwt(credentials.credentials):
                raise AuthError(detail="Invalid token or expired token.")

            return credentials.credentials

        else:
            raise AuthError(detail="Invalid authorization code.")
