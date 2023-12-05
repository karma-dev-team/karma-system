from app.auth.session import AbstractAuthSession
from app.user.entities import UserEntity


def auth_session_provider() -> AbstractAuthSession:
    ...


def user_provider() -> UserEntity:
    ... 
