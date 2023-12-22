from fastapi import FastAPI, APIRouter
from sqlalchemy.orm import registry as registry_class

from app.files.models import load_models
from . import routes
from .file_storage.base import AbstractFileStorage
from .providers import file_storage_provider


def load_module(
    app: FastAPI,
    router: APIRouter,
    registry: registry_class,
    file_storage: AbstractFileStorage,
):
    app.dependency_overrides[file_storage_provider] = lambda: file_storage

    router.include_router(routes.router)

    load_models(registry)
