from typing import Tuple
from datetime import datetime, timedelta

import jwt

from core.settings import get_settings


class AuthUtils:
    @staticmethod
    def create_access_token(subject: dict) -> Tuple[str, str]:

        expire = datetime.now() + timedelta(
            minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES
        )

        payload = {"exp": expire, **subject}
        encoded_jwt = jwt.encode(
            payload,
            get_settings().SECRET_KEY.get_secret_value(),
            algorithm=get_settings().ALGORITHM,
        )
        expiration_datetime = expire.strftime(get_settings().DATETIME_FORMAT)
        return encoded_jwt, expiration_datetime

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return get_settings().PWD_CONTEXT.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return get_settings().PWD_CONTEXT.hash(password)

    @staticmethod
    def decode_jwt(token: str) -> dict:

        try:
            decoded_token = jwt.decode(
                token,
                get_settings().SECRET_KEY.get_secret_value(),
                algorithms=get_settings().ALGORITHM,
            )

            if decoded_token["exp"] >= int(round(datetime.now().timestamp())):
                return decoded_token
            else:
                return {}

        except Exception:
            return {}

    @staticmethod
    def verify_jwt(jwt_token: str) -> bool:

        try:
            payload = AuthUtils.decode_jwt(jwt_token)

        except Exception:
            return False

        if payload:
            return True

        return False
