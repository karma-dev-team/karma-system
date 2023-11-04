import uvicorn
from fastapi import FastAPI

from app.infrastructure.api.app import create_app
from app.infrastructure.config import load_config
from app.infrastructure.database import load_database
from app.infrastructure.logging.logger import configure_logging
from app.module.module import configure_module_loader


def get_app() -> FastAPI:
	config = load_config('./deploy/config.toml')
	session, registry = load_database(config.db)

	app, router = create_app(config.api, config.debug)
	app.logger = configure_logging(config.logging)

	module = configure_module_loader(workflow_data={
		'registry': registry,
		'app': app,
		'session': session,
		'router': router,
	})
	module.load()

	return app


app = get_app()
