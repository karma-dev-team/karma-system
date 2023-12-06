from __future__ import annotations
from typing import TYPE_CHECKING, Annotated

from fastapi import FastAPI, Depends

from app.acl.access_policy import BasicAccessPolicy
from app.auth.providers import user_provider, optional_user
from app.base.api.ioc import ioc_provider
from app.base.api.providers import uow_provider, config_provider, event_dispatcher_provider
from app.base.config import GlobalConfig
from app.base.database.uow import SQLAlchemyUoW
from app.base.events.dispatcher import EventDispatcher
from app.base.ioc import AbstractIoContainer

from app.karma.services import KarmaService
from app.server.services import ServerService, PlayerService
from app.user.entities import UserEntity
from app.user.services import UserService

if TYPE_CHECKING:
    from app.server.interfaces.service import AbstractServerService, AbstractPlayerService
    from app.karma.interfaces.services import AbstractKarmaService
    from app.user.interfaces import AbstractUserService


class IoContainerImpl(AbstractIoContainer):
    def __init__(
        self,
        uow: SQLAlchemyUoW,
        event_dispatcher: EventDispatcher,
        config: GlobalConfig,
        user: UserEntity | None,
    ):
        self.uow = uow
        self.config = config
        self.event_dispatcher = event_dispatcher
        self.user = user

    def user_service(self) -> AbstractUserService:
        return UserService(
            uow=self.uow,
            event_dispatcher=self.event_dispatcher
        )

    def karma_service(self) -> AbstractKarmaService:
        return KarmaService(
            uow=self.uow,
            event_dispatcher=self.event_dispatcher,
            server_uow=self.uow,
        )

    def server_service(self) -> AbstractServerService:
        return ServerService(
            uow=self.uow,
            game_uow=self.uow,
            event_dispatcher=self.event_dispatcher,
            config=self.config.security,
            access_policy=BasicAccessPolicy(self.user)
        )

    def player_service(self) -> AbstractPlayerService:
        return PlayerService()


async def get_ioc(
    event_dispatcher: Annotated[EventDispatcher, Depends(event_dispatcher_provider)],
    uow: Annotated[SQLAlchemyUoW, Depends(uow_provider)],
    config: Annotated[GlobalConfig, Depends(config_provider)],
    user: Annotated[UserEntity | None, Depends(optional_user)]
) -> IoContainerImpl:
    return IoContainerImpl(
        event_dispatcher=event_dispatcher,
        uow=uow,
        config=config,
        user=user,
    )


def load_ioc(app: FastAPI):
    app.dependency_overrides[ioc_provider] = get_ioc
