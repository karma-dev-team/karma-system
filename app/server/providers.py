from fastapi import FastAPI

from app.server.entities.server import ServerEntity


async def server_provider() -> ServerEntity:
	...


def load_providers(app: FastAPI) -> None:
	from .dependencies import get_server

	app.dependency_overrides[server_provider] = get_server
