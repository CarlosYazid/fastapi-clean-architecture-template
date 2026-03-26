from core.exceptions import AuthError
from model.user import User
from repository.abc import Repository
from schema.user import UserRead
from schema.auth import SignIn, SignUp, SignInResponse
from services.abc import BaseService
from util.auth import AuthUtils


class AuthService(BaseService):
    def __init__(self, user_repository: Repository):
        super().__init__(user_repository)

    async def sign_in(self, sign_in_info: SignIn) -> SignInResponse:

        user: User = await self._repository.read_by_email(sign_in_info.email)

        if not user.is_active:
            raise AuthError(detail="Account is not active")

        if not AuthUtils.verify_password(sign_in_info.password, user.password):
            raise AuthError(detail="Incorrect email or password")

        user_info = UserRead(**user.model_dump())

        access_token, expiration_datetime = AuthUtils.create_access_token(user_info.dict())

        return SignInResponse(
            access_token=access_token,
            expiration=expiration_datetime,
            user_info=user_info,
        )

    async def sign_up(self, user_info: SignUp) -> User:

        user = User(**user_info.dict(exclude_none=True), is_active=True, is_superuser=False)

        user.password = AuthUtils.get_password_hash(user_info.password)

        return await self._repository.create(user)
