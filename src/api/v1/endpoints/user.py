from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi_querybuilder import QueryBuilder
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import apaginate

from core.database import Database
from core.container import Container
from core.dependencies import get_current_super_user
from core.security import JWTBearer
from model.user import User
from schema import UserRead, UserUpdate, UserCreate
from services.user import UserService

router = APIRouter(prefix="/user", tags=["user"], dependencies=[Depends(JWTBearer())])

@router.get("", response_model=Page[UserRead])
@inject
async def _list(
    query=QueryBuilder(User),
    db: Database = Depends(Provide[Container.db]),
    _: User = Depends(get_current_super_user)):
    
    async with db.session() as session:
        return await apaginate(session, query)

@router.get("/{user_id}", response_model=UserRead)
@inject
async def read(
    user_id: int,
    service: UserService = Depends(Provide[Container.user_service]),
    _: User = Depends(get_current_super_user)):

    return await service.read(user_id)


@router.post("", response_model=UserRead)
@inject
async def create(
    user: UserCreate,
    service: UserService = Depends(Provide[Container.user_service]),
    _: User = Depends(get_current_super_user)):

    return await service.create(user)


@router.patch("", response_model=UserRead)
@inject
async def update(
    user: UserUpdate,
    service: UserService = Depends(Provide[Container.user_service]),
    _: User = Depends(get_current_super_user)):

    return await service.update(user.id, user)


@router.delete("/{user_id}")
@inject
async def delete(
    user_id: int,
    service: UserService = Depends(Provide[Container.user_service]),
    _: User = Depends(get_current_super_user),
):

    return await service.delete(user_id)
