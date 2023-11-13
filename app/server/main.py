from fastapi import APIRouter

from . import _routes


def load_module(router: APIRouter):
	router.include_router(_routes.router)
