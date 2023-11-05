from typing import Tuple

from fastapi import FastAPI, APIRouter

from app.infrastructure.api.config import APIConfig


def create_app(config: APIConfig, debug: bool = True) -> Tuple[FastAPI, APIRouter]:
    router = APIRouter()

    app = FastAPI(**config.fastapi_kwargs, debug=debug)

    return app, router
