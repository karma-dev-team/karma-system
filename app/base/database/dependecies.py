from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from app.base.api.providers import session_provider
from app.base.database.uow import SQLAlchemyUoW


def uow_dependency(
    request: Request,
):
    return SQLAlchemyUoW.create(request.app.state.db_session)
