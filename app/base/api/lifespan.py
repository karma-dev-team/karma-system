from contextlib import asynccontextmanager

from aiohttp import ClientSession
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.base.database.main import init_pgtrgm


def lifespan(db_session: async_sessionmaker):
    @asynccontextmanager
    async def inner(app: FastAPI):
        app.state.db_session = db_session()
        await init_pgtrgm(app.state.db_session)
        yield
        await app.state.db_session.close()

    return inner
