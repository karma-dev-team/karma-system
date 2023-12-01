from typing import Annotated

from fastapi import Request, Header, Depends

from app.base.api.providers import ioc_provider
from app.base.ioc import AbstractIoContainer
from app.server.entities.server import ServerEntity
from app.server.exceptions import IncorrectAPIServerToken


async def get_server(
	request: Request,
	ioc_container: Annotated[AbstractIoContainer, Depends(ioc_provider)],
	server_token: str = Header(..., convert_underscores=False, alias='X-Api-Token'),
) -> ServerEntity:
	if not server_token or not server_token.startswith('Bearer'):
		raise IncorrectAPIServerToken("Incorrect token")

