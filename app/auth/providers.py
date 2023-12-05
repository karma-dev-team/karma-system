from app.auth.session import AbstractAuthSession


def auth_session_provider() -> AbstractAuthSession:
    ...
