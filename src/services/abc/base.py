from typing import Any

from repository.abc.contracts import Repository


class BaseService:
    def __init__(self, repository: Repository) -> None:
        self._repository = repository

    async def read(self, id: int) -> Any:
        return await self._repository.read(id)

    async def create(self, schema: Any) -> Any:
        return await self._repository.create(schema)

    async def update(self, id: int, schema: Any) -> Any:
        return await self._repository.update(id, schema)

    async def update_attr(self, id: int, attr: str, value: Any) -> Any:
        return await self._repository.update_attr(id, attr, value)

    async def put_update(self, id: int, schema: Any) -> Any:
        return await self._repository.put_update(id, schema)

    async def delete(self, id: int) -> Any:
        return await self._repository.delete(id)
