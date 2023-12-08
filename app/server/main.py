from fastapi import APIRouter, FastAPI

from . import _routes
from .events.main import load_event_dispatcher
from .providers import load_providers
from ..base.events.dispatcher import EventDispatcher


def load_module(router: APIRouter, app: FastAPI, event_dispatcher: EventDispatcher):
	router.include_router(_routes.server_router)
	router.include_router(_routes.player_router)

	load_providers(app)

	load_event_dispatcher(event_dispatcher)
