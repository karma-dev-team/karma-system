from typing import Tuple

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import registry as registry_class

from app.infrastructure.database.base import create_registry, sa_session_factory, setup_engine
from app.infrastructure.database.config import DatabaseConfig


def load_database(config: DatabaseConfig) -> Tuple[async_sessionmaker, registry_class]:
	registry = create_registry()
	engine = setup_engine(config.database_dsn)
	session = sa_session_factory(engine)

	return session, registry
