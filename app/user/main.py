from fastapi import APIRouter
from sqlalchemy.orm import registry as reg_class

from . import _routes, _models


def load_module(router: APIRouter, registry: reg_class):
	router.include_router(_routes.router)

	_models.load_models(registry)
