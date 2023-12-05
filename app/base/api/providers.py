from sqlalchemy.ext.asyncio import AsyncSession

from app.base.config import GlobalConfig
from app.base.database.uow import SQLAlchemyUoW
from app.base.ioc import AbstractIoContainer


def ioc_provider() -> AbstractIoContainer:
	...


def config_provider() -> GlobalConfig:
	...


def uow_provider() -> SQLAlchemyUoW:
	...


def session_provider() -> AsyncSession:
	...
