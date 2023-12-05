from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.base.api.providers import session_provider
from app.base.database.uow import SQLAlchemyUoW


def uow_dependency(
    session: Annotated[AsyncSession, Depends(session_provider)],
):
    return SQLAlchemyUoW.create(session)
