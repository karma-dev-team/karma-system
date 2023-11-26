from fastapi import FastAPI

from app.base.api.providers import ioc_provider
from app.base.ioc import AbstractIoContainer
from app.karma.interfaces.services import AbstractKarmaService
from app.karma.services import KarmaService
from app.user.services import UserService
from app.user.interfaces import AbstractUserService


class IoContainerImpl(AbstractIoContainer):
    def user_service(self) -> AbstractUserService:
        return UserService()

    def karma_service(self) -> AbstractKarmaService:
        return KarmaService()


async def get_ioc() -> IoContainerImpl:
    return IoContainerImpl()


def load_ioc(app: FastAPI):
    app.dependency_overrides[ioc_provider()] = get_ioc
