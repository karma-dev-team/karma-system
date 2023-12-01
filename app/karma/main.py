from fastapi import APIRouter

from .events.main import load_handler_events
from .models import load_models
from . import routes
from ..base.events.dispatcher import EventDispatcher


def load_module(registry, router: APIRouter, event_dispatcher: EventDispatcher):
	router.include_router(routes.router)

	load_models(registry)
	load_handler_events(event_dispatcher)
