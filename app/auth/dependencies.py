from typing import Annotated, Callable
from uuid import UUID

from fastapi import Request, Depends

from app.auth.consts import AUTH_KEY
from app.auth.exceptions import AccessDenied
from app.auth.providers import auth_session_provider, user_provider
from app.auth.session import AbstractAuthSession
from app.base.api.providers import uow_provider
from app.base.database.uow import SQLAlchemyUoW
from app.user.entities import UserEntity
from app.user.enums import UserRoles
from app.user.value_objects import UserID


async def user(
    request: Request,
    auth_session: Annotated[AbstractAuthSession, Depends(auth_session_provider)],
    uow: Annotated[SQLAlchemyUoW, Depends(uow_provider)]
) -> UserEntity:
    session_id = request.cookies.get(AUTH_KEY, None)
    if not session_id:
        raise AccessDenied

    user_id = await auth_session.get(session_id)
    if not user_id:
        raise AccessDenied
    user_id = UserID.from_uuid(UUID(user_id))
    return await uow.user.get_user_by_id(user_id=user_id)


def role_required(*roles: UserRoles) -> Callable:
    async def inner(
        user: Annotated[UserEntity, Depends(user_provider)],
    ) -> None:
        if roles not in user.role:
            raise AccessDenied
    return inner
