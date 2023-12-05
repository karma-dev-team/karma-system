from typing import Annotated

from app.base.api.providers import ioc_provider
from app.base.ioc import AbstractIoContainer
from app.user.entities import UserEntity


def user(
    ioc: Annotated[AbstractIoContainer, ioc_provider],
) -> UserEntity:
    ...
