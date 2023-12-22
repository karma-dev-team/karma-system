from __future__ import annotations
from typing import TYPE_CHECKING

from aiohttp import ClientSession
from sqlalchemy.ext.asyncio import AsyncSession

from app.base.events.dispatcher import EventDispatcher

if TYPE_CHECKING:
	from app.base.config import GlobalConfig
	from app.base.database.uow import SQLAlchemyUoW


def config_provider() -> GlobalConfig:
	...


def uow_provider() -> SQLAlchemyUoW:
	...


def session_provider() -> AsyncSession:
	...


def event_dispatcher_provider() -> EventDispatcher:
	...


def http_client_provider() -> ClientSession:
	...
