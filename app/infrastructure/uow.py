from contextlib import asynccontextmanager
from typing import AsyncGenerator, Protocol


class IUoW(Protocol):
    async def commit(self) -> None:
        ...

    async def rollback(self) -> None:
        ...

    @asynccontextmanager
    async def transaction(self) -> AsyncGenerator[None, None]:
        ...
