from fastapi import APIRouter
from sqlalchemy.orm import registry as reg_class

from app.base.events.dispatcher import EventDispatcher
from . import _routes, models, _events


def load_module(router: APIRouter, registry: reg_class, event_dispatcher: EventDispatcher):
	router.include_router(_routes.router, tags=["user"])

	models.load_models(registry)
	_events.load_handler_events(event_dispatcher)
