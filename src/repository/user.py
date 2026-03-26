from typing import Callable
from contextlib import AbstractContextManager

from pydantic import EmailStr
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from model.user import User
from core.exceptions import NotFoundError
from repository.abc import BaseRepository


class UserRepository(BaseRepository):
    def __init__(
        self, session_factory: Callable[..., AbstractContextManager[AsyncSession]]
    ):
        super().__init__(session_factory, User)

    async def read_by_email(self, email: EmailStr) -> User:
        
        async with self.session_factory() as session:

            query = (
                await session
                .exec(select(self.model)
                .where(self.model.email == email))
            )
            
            result = query.first()

            if not result:
                raise NotFoundError(detail=f"Not found {self.model.__name__} by {id}")

            return result
