from fastapi import APIRouter, FastAPI

from app.auth.session import MemoryAuthSession
from . import routes
from .dependencies import user
from .providers import auth_session_provider, user_provider


def load_module(router: APIRouter, app: FastAPI):
    session = MemoryAuthSession()

    app.dependency_overrides[auth_session_provider] = lambda: session
    app.dependency_overrides[user_provider] = user

    router.include_router(routes.router)

