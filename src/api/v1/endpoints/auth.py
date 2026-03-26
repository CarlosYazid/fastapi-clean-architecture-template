from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from src.core.container import Container
from src.core.dependencies import get_current_active_user
from src.services.auth import AuthService
from src.model.user import User
from src.schema.user import UserRead
from src.schema.auth import SignIn, SignInResponse, SignUp

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/sign-in", response_model=SignInResponse)
@inject
async def sign_in(user_info: SignIn, service: AuthService = Depends(Provide[Container.auth_service])):
    return await service.sign_in(user_info)


@router.post("/sign-up", response_model=UserRead)
@inject
async def sign_up(user_info: SignUp, service: AuthService = Depends(Provide[Container.auth_service])):
    return await service.sign_up(user_info)


@router.get("/me", response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user
