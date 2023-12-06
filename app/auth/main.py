from fastapi import APIRouter, FastAPI

from app.auth.session import MemoryAuthSession


def load_module(router: APIRouter, app: FastAPI):
    from . import routes
    from .dependencies import user
    from .providers import auth_session_provider, user_provider

    session = MemoryAuthSession()

    app.dependency_overrides[auth_session_provider] = lambda: session
    app.dependency_overrides[user_provider] = user

    router.include_router(routes.router)

