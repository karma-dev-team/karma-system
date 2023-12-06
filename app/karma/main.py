from fastapi import APIRouter

from app.base.events.dispatcher import EventDispatcher


def load_module(registry, router: APIRouter, event_dispatcher: EventDispatcher):
	from .events.main import load_handler_events
	from .models import load_models
	from . import routes

	router.include_router(routes.router)

	load_models(registry)
	load_handler_events(event_dispatcher)
