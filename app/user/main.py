from . import _routes


def load_module(router):
	router.include_router(_routes.router)
