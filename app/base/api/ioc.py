from fastapi import FastAPI

from app.base.api.providers import ioc_provider
from app.base.ioc import AbstractIoContainer
from app.user.interfaces import AbstractUserService


class IoContainerImpl(AbstractIoContainer):
	def user_service(self) -> AbstractUserService:
		pass


async def get_ioc() -> IoContainerImpl:
	return IoContainerImpl()


def setup_ioc_container(app: FastAPI):
	app.dependency_overrides[ioc_provider] = get_ioc
