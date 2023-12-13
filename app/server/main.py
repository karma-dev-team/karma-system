from fastapi import APIRouter, FastAPI
from sqlalchemy.orm import registry as registry_class

from . import _routes
from .events.main import load_event_dispatcher
from .providers import load_providers
from ..base.events.dispatcher import EventDispatcher
from .models import load_models


def load_module(router: APIRouter, app: FastAPI, event_dispatcher: EventDispatcher, registry: registry_class):
	router.include_router(_routes.server_router)
	router.include_router(_routes.player_router)

	load_providers(app)

	load_models(registry)

	load_event_dispatcher(event_dispatcher)
