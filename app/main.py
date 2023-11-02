from fastapi import FastAPI, APIRouter

from app.infrastructure.database import load_database
from app.module.module import configure_module_loader


def get_app() -> FastAPI:
	config = load_config()
	registry, session = load_database(config)

	app = FastAPI()

	router = APIRouter()
	app.include_router(router)

	module = configure_module_loader(workflow_data={
		'registry': registry,
		'app': app,
		'session': session,
	})
	module.load()

	return app

