from fastapi import APIRouter
from sqlalchemy.orm import registry as registry_class

from app.games.models import load_models
from app.games import routes


def load_module(registry: registry_class, router: APIRouter) -> None:
	router.include_router(routes.router)

	load_models(registry)
