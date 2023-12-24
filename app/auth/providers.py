from typing import TYPE_CHECKING, Union

from app.auth.mailing.base import AbstractMailing

if TYPE_CHECKING:
    from app.auth.session import AbstractAuthSession
    from app.user.entities import UserEntity


def auth_session_provider() -> "AbstractAuthSession":
    ...


def user_provider() -> "UserEntity":
    ... 


def optional_user() -> Union["UserEntity", None]:
    ...


def mailing_provider() -> AbstractMailing:
    ...
