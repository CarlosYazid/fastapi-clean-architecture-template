from fastapi import APIRouter

from api.v1.endpoints import UserRouter, AuthRouter

routers = APIRouter(tags=["v1"])

routers.include_router(UserRouter)
routers.include_router(AuthRouter)
