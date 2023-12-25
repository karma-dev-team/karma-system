from __future__ import annotations
from typing import TYPE_CHECKING, Annotated

from aiohttp import ClientSession
from fastapi import FastAPI, Depends

from app.auth.access_policy import BasicAccessPolicy
from app.auth.interfaces import AbstractAuthService
from app.auth.mailing.base import AbstractMailing
from app.auth.providers import optional_user, mailing_provider
from app.auth.service import AuthService
from app.base.api.ioc import ioc_provider
from app.base.api.providers import uow_provider, config_provider, event_dispatcher_provider, http_client_provider
from app.base.config import GlobalConfig
from app.base.database.uow import SQLAlchemyUoW
from app.base.events.dispatcher import EventDispatcher
from app.base.ioc import AbstractIoContainer
from app.files.file_storage.base import AbstractFileStorage
from app.files.interfaces.services import FileService
from app.files.providers import file_storage_provider
from app.files.services import FileServiceImpl
from app.games.interfaces.service import AbstractCategoryService, AbstractGameService
from app.games.services import GameService, CategoryService

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
        file_storage: AbstractFileStorage,
        session: ClientSession,
        user: UserEntity | None,
        mailing_adapter: AbstractMailing,
    ):
        self.uow = uow
        self.session = session
        self.config = config
        self.event_dispatcher = event_dispatcher
        self.user = user
        self.file_storage = file_storage
        self.mailing_adapter = mailing_adapter

    def user_service(self) -> AbstractUserService:
        return UserService(
            uow=self.uow,
            event_dispatcher=self.event_dispatcher,
            access_policy=BasicAccessPolicy(self.user),
            config=self.config,
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
            access_policy=BasicAccessPolicy(self.user),
            file_service=self.file_service(),
        )

    def player_service(self) -> AbstractPlayerService:
        return PlayerService(
            uow=self.uow,
            event_dispatcher=self.event_dispatcher,
        )

    def category_service(self) -> AbstractCategoryService:
        return CategoryService(
            uow=self.uow,
            event_dispatcher=self.event_dispatcher,
            access_policy=BasicAccessPolicy(self.user)
        )

    def game_service(self) -> AbstractGameService:
        return GameService(
            uow=self.uow,
            event_dispatcher=self.event_dispatcher,
            access_policy=BasicAccessPolicy(self.user)
        )

    def file_service(self) -> FileService:
        return FileServiceImpl(
            uow=self.uow,
            file_storage=self.file_storage,
            session=self.session,
        )

    def auth_service(self) -> AbstractAuthService:
        return AuthService(
            uow=self.uow,
            event_dispatcher=self.event_dispatcher,
            email_adapter=self.mailing_adapter,
            config=self.config,
        )


async def get_ioc(
    event_dispatcher: Annotated[EventDispatcher, Depends(event_dispatcher_provider)],
    uow: Annotated[SQLAlchemyUoW, Depends(uow_provider)],
    config: Annotated[GlobalConfig, Depends(config_provider)],
    file_storage: Annotated[AbstractFileStorage, Depends(file_storage_provider)],
    user: Annotated[UserEntity | None, Depends(optional_user)],
    client_session: Annotated[ClientSession, Depends(http_client_provider)],
    mailing_adapter: Annotated[AbstractMailing, Depends(mailing_provider)]
) -> IoContainerImpl:
    return IoContainerImpl(
        event_dispatcher=event_dispatcher,
        uow=uow,
        config=config,
        user=user,
        file_storage=file_storage,
        session=client_session,
        mailing_adapter=mailing_adapter,
    )


def load_ioc(app: FastAPI):
    app.dependency_overrides[ioc_provider] = get_ioc
