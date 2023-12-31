from fastapi import APIRouter, FastAPI
from sqlalchemy.orm import registry as registry_class

from .events.main import load_event_dispatcher
from .providers import load_providers
from ..base.events.dispatcher import EventDispatcher
from .models import load_models


def load_module(router: APIRouter, app: FastAPI, event_dispatcher: EventDispatcher, registry: registry_class):
	from . import _routes

	router.include_router(_routes.server_router, tags=["server"])
	router.include_router(_routes.player_router, tags=["player"])

	load_providers(app)

	load_models(registry)

	load_event_dispatcher(event_dispatcher)
