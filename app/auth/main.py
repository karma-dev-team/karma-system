from fastapi import APIRouter, FastAPI

from app.auth.session import MemoryAuthSession, load_redis

from . import routes
from .dependencies import user, _optional_user
from .providers import auth_session_provider, user_provider, optional_user


def load_module(router: APIRouter, app: FastAPI, config):

    session = load_redis(config.redis)

    app.dependency_overrides[auth_session_provider] = lambda: session
    app.dependency_overrides[user_provider] = user
    app.dependency_overrides[optional_user] = _optional_user

    router.include_router(routes.router)
