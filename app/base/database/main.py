from typing import Tuple

from fastapi import FastAPI
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


async def init_pgtrgm(app: FastAPI, workflow_data: dict):
	logger = workflow_data['logger']
	session = app.state.db_session
	async with session.begin():
		await session.execute(text('CREATE EXTENSION IF NOT EXISTS pg_trgm'))
		logger.info("pg_trgm loaded in postgresql")
		# await session.execute(select(func.set_limit('0.01')))


async def init_session(app: FastAPI, workflow_data: dict):
	workflow_data['logger'].info("Initialized db session")
	app.state.db_session = workflow_data['session']()


async def shutdown_session(app: FastAPI, workflow_data: dict):
	workflow_data['logger'].info("Shutting down db session")
	await app.state.db_session.close()
