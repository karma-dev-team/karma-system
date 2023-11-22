from fastapi import Request, Header

from app.server.entities.server import ServerEntity
from app.server.exceptions import IncorrectAPIServerToken


async def get_server(
	request: Request,
	server_token: str = Header(..., convert_underscores=False, alias='Authorization')
) -> ServerEntity:
	if not server_token or not server_token.startswith('Bearer'):
		raise IncorrectAPIServerToken("Incorrect token")


