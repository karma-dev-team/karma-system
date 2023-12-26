from typing import Tuple

from fastapi import FastAPI, APIRouter

from app.base.api.config import APIConfig
from app.base.api.exception import load_basic_exceptions_handlers
from app.base.api.middlewares.main import load_middlewares


def create_app(config: APIConfig, debug: bool = True, lifespan: callable = None) -> Tuple[FastAPI, APIRouter]:
    router = APIRouter()

    app = FastAPI(**config.fastapi_kwargs, debug=debug, lifespan=lifespan)

    load_basic_exceptions_handlers(app)
    load_middlewares(app, debug)

    return app, router
