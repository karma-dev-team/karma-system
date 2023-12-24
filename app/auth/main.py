from typing import Callable

from fastapi import APIRouter, FastAPI

from . import models
from . import routes
from .dependencies import user, _optional_user, auth_session_database
from .lifespan import auth_lifespan
from .mailing.yandex import load_yandex_mailing
from .providers import auth_session_provider, user_provider, optional_user, mailing_provider


def load_module(router: APIRouter, app: FastAPI, config, registry, lifespan_callbacks: list[Callable]):
    # session = load_redis(config.redis)
    yandex_mailing = load_yandex_mailing(config.mailing)
    lifespan_callbacks.append(auth_lifespan)

    app.dependency_overrides[auth_session_provider] = auth_session_database
    app.dependency_overrides[user_provider] = user
    app.dependency_overrides[optional_user] = _optional_user
    app.dependency_overrides[mailing_provider] = lambda: yandex_mailing

    models.load_models(registry)
    router.include_router(routes.router, tags=["auth"])
