from typing import Tuple

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.orm import registry as registry_class

from app.base.database.base import create_registry, sa_session_factory, setup_engine
from app.base.database.config import DatabaseConfig


def load_database(config: DatabaseConfig) -> Tuple[async_sessionmaker, registry_class]:
	registry = create_registry()
	engine = setup_engine(config.database_dsn)
	session = sa_session_factory(engine)

	return session, registry


async def init_pgtrgm(session: AsyncSession):
	async with session.begin():
		await session.execute(text('CREATE EXTENSION IF NOT EXISTS pg_trgm'))
		# await session.execute(select(func.set_limit('0.01')))
