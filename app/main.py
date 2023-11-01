def get_app() -> FastAPI:
	load_database()

	load_value_objects()

	app = FastAPI()

	router = APIRouter()
	app.include_router(router)

	load_providers(app)
	load_routes(router)

	return app

