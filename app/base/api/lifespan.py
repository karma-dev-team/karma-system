from contextlib import asynccontextmanager
from typing import Callable, Mapping, Any

from aiohttp import ClientSession
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.base.database.main import init_pgtrgm


def lifespan(callbacks: list[Callable], workflow_data: Mapping[str, Any]):
    @asynccontextmanager
    async def inner(app: FastAPI):
        for callback in callbacks:
            app.state.db_session = db_session()
            await init_pgtrgm(app.state.db_session)
        yield
        await app.state.db_session.close()

    return inner
