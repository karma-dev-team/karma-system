from aiohttp import ClientSession
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.auth.lifespan import init_mailing, shutdown_mailing
from app.auth.mailing.yandex import load_yandex_mailing
from app.base.api.app import create_app
from app.base.api.lifespan import lifespan
from app.base.api.providers import config_provider, uow_provider, session_provider, event_dispatcher_provider, \
	http_client_provider
from app.base.config import load_config
from app.base.database import load_database
from app.base.database.dependecies import uow_dependency
from app.base.database.main import init_pgtrgm, shutdown_session, init_session
from app.base.events.main import configure_event_dispatcher
from app.base.logging.logger import configure_logging, get_logger
from app.base.api.ioc_impl import load_ioc
from app.files.file_storage.local_storage import LocalStorage, configure_file_storage
from app.module.module import configure_module_loader
from app.templating.main import load_templating
from app.base.api.router import router as base_router


def get_app() -> FastAPI:
	config = load_config('./deploy/config.toml')
	configure_logging(config.logging)
	logger = get_logger(__name__)
	session, registry = load_database(config.db)

	# the reason why we don't pass callbacks to modules
	# is because lifespan property in routing.Router
	# needs complex initialization
	yandex_mailing = load_yandex_mailing(config.mailing)
	lifespan_func = lifespan(
		startup_callbacks=[
			init_session,
			init_pgtrgm,
			init_mailing,
		],
		shutdown_callbacks=[
			shutdown_session,
			shutdown_mailing,
		],
		workflow_data={
			'session': session,
			'registry': registry,
			'config': config,
			'logger': logger,
			'email_adapter': yandex_mailing,
		}
	)
	app, router = create_app(config.api, config.debug, lifespan=lifespan_func)
	event_dispatcher = configure_event_dispatcher()
	file_storage = configure_file_storage()
	client_session = ClientSession()

	# exclude
	app.mount("/static", StaticFiles(directory="static"), name="static")
	app.dependency_overrides[http_client_provider] = lambda: client_session
	app.dependency_overrides[session_provider] = lambda: session()
	app.dependency_overrides[uow_provider] = uow_dependency
	app.dependency_overrides[config_provider] = lambda: config
	app.dependency_overrides[event_dispatcher_provider] = lambda: event_dispatcher

	# preload ioc
	load_ioc(app)
	load_templating(app, template_directory="./static/templates")

	modules = configure_module_loader(workflow_data={
		'registry': registry,
		'app': app,
		'event_dispatcher': event_dispatcher,
		'session': session,
		'router': router,
		'config': config,
		'file_storage': file_storage,
		'email_adapter': yandex_mailing,
	})
	modules.load()

	app.include_router(base_router)
	app.include_router(router)

	return app


# use this for proper logging
app = get_app()
