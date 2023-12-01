from fastapi import FastAPI

from app.server.entities.server import ServerEntity
from .dependencies import get_server


async def server_provider() -> ServerEntity:
	...


def load_providers(app: FastAPI) -> None:
	app.dependency_overrides[server_provider] = get_server
