from contextlib import AbstractContextManager
from typing import Any, Callable, Type, TypeVar

from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, update, delete

from core.exceptions import DuplicatedError, NotFoundError
from model.abc.base import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseRepository:
    def __init__(
        self,
        session_factory: Callable[..., AbstractContextManager[AsyncSession]],
        model: Type[T],
    ) -> None:
        self.session_factory = session_factory
        self.model = model

    async def read(self, id: int) -> T:

        async with self.session_factory() as session:
            query = await session.exec(select(self.model).where(self.model.id == id))

            result = query.first()

            if not result:
                raise NotFoundError(detail=f"Not found {self.model.__name__} by {id}")

            return result

    async def create(self, schema: T) -> T:

        entity = self.model(**schema.dict())

        try:
            async with self.session_factory() as session:
                session.add(entity)
                await session.commit()
                await session.refresh(entity)

        except IntegrityError as e:
            raise DuplicatedError(detail=str(e.orig))

        return entity

    async def update(self, id: int, schema: T) -> T:

        async with self.session_factory() as session:
            result = await session.exec(
                update(self.model)
                .where(self.model.id == id)
                .values(**schema.dict(exclude_none=True))
                .returning(self.model)
            )

            updated = result.first()

            if not updated:
                raise NotFoundError(detail=f"Not found {self.model.__name__} by {id}")

        return updated

    async def update_attr(self, id: int, column: str, value: Any) -> T:

        async with self.session_factory() as session:
            result = await session.exec(
                update(self.model)
                .where(self.model.id == id)
                .values(**{column: value})
                .returning(self.model)
            )

            updated = result.first()

            if not updated:
                raise NotFoundError(detail=f"Not found {self.model.__name__} by {id}")

        return updated

    async def whole_update(self, id: int, schema: T) -> T:

        async with self.session_factory() as session:
            result = await session.exec(
                update(self.model)
                .where(self.model.id == id)
                .values(**schema.dict(exclude_none=True))
                .returning(self.model)
            )

            updated = result.first()

            if not updated:
                raise NotFoundError(detail=f"Not found {self.model.__name__} by {id}")

        return updated

    async def delete(self, id: int):

        async with self.session_factory() as session:
            await session.exec(delete(self.model).where(self.model.id == id))
