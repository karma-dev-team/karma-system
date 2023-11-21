from fastapi import APIRouter

from .models import load_models
from . import routes


def load_module(registry, router: APIRouter):
	router.include_router(routes.router)

	load_models(registry)
