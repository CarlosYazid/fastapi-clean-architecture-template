from typing import Any, AsyncGenerator
from contextlib import AbstractContextManager, asynccontextmanager

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


class Database:
    def __init__(self, db_url: str) -> None:
        self._engine = create_async_engine(db_url, echo=True)
        self._session_factory = async_sessionmaker(
            class_=AsyncSession,
            autocommit=False,
            autoflush=False,
            bind=self._engine,
        )

    @asynccontextmanager
    async def session(
        self,
    ) -> AsyncGenerator[Any, AbstractContextManager[AsyncSession]]:
        async with self._session_factory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
