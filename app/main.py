from fastapi import FastAPI, APIRouter

from app.module.module import configure_module_loader


def get_app() -> FastAPI:
	registry, session = load_database()

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

