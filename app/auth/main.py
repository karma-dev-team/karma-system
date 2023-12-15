from fastapi import APIRouter, FastAPI

from . import models
from . import routes
from .dependencies import user, _optional_user, auth_session_database
from .providers import auth_session_provider, user_provider, optional_user


def load_module(router: APIRouter, app: FastAPI, config, registry):
    # session = load_redis(config.redis)

    app.dependency_overrides[auth_session_provider] = auth_session_database
    app.dependency_overrides[user_provider] = user
    app.dependency_overrides[optional_user] = _optional_user

    models.load_models(registry)
    router.include_router(routes.router, tags=["auth"])
