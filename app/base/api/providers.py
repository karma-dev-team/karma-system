from sqlalchemy.ext.asyncio import AsyncSession

from app.base.config import GlobalConfig
from app.base.database.uow import SQLAlchemyUoW


def config_provider() -> GlobalConfig:
	...


def uow_provider() -> SQLAlchemyUoW:
	...


def session_provider() -> AsyncSession:
	...
