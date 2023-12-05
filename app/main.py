from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.base.api.app import create_app
from app.base.api.providers import config_provider
from app.base.config import load_config
from app.base.database import load_database
from app.base.events.main import configure_event_dispatcher
from app.base.logging.logger import configure_logging
from app.base.api.ioc_impl import load_ioc
from app.module.module import configure_module_loader
from app.templating.main import load_templating


def get_app() -> FastAPI:
	config = load_config('./deploy/config.toml')
	session, registry = load_database(config.db)

	app, router = create_app(config.api, config.debug)
	configure_logging(config.logging)
	event_dispatcher = configure_event_dispatcher()

	# exclude
	app.mount("/static", StaticFiles(directory="static"), name="static")
	app.dependency_overrides[config_provider] = lambda: config

	# preload ioc
	load_ioc(app)
	load_templating(app, template_directory="templates")

	module = configure_module_loader(workflow_data={
		'registry': registry,
		'app': app,
		'event_dispatcher': event_dispatcher,
		'session': session,
		'router': router,
	})
	module.load()

	app.include_router(router, prefix="/")

	return app


# use this for proper logging
app = get_app()
