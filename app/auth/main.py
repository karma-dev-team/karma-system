from typing import Callable

from fastapi import APIRouter, FastAPI

from . import models
from . import routes
from .dependencies import user, _optional_user, auth_session_database
from .mailing.base import AbstractMailing
from .mailing.yandex import load_yandex_mailing
from .providers import auth_session_provider, user_provider, optional_user, mailing_provider


def load_module(router: APIRouter, app: FastAPI, config, registry, email_adapter: AbstractMailing):
    # session = load_redis(config.redis)

    app.dependency_overrides[auth_session_provider] = auth_session_database
    app.dependency_overrides[user_provider] = user
    app.dependency_overrides[optional_user] = _optional_user
    app.dependency_overrides[mailing_provider] = lambda: email_adapter

    models.load_models(registry)
    router.include_router(routes.router, tags=["auth"])
