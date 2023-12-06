from typing import Annotated

from fastapi import Header, Depends

from app.base.api.providers import config_provider, uow_provider
from app.base.config import GlobalConfig
from app.base.database.uow import SQLAlchemyUoW
from app.server.entities.server import ServerEntity
from app.server.exceptions import IncorrectAPIServerToken, ServerNotExists
from app.server.interfaces.persistance import GetServerFilter
from app.server.security import decode_jwt
from app.server.value_objects.ids import ServerID


async def get_server(
	uow: Annotated[SQLAlchemyUoW, Depends(uow_provider)],
	config: Annotated[GlobalConfig, Depends(config_provider)],
	server_token: str = Header(..., convert_underscores=False, alias='X-Api-Token'),
) -> ServerEntity:
	if not server_token or not server_token.startswith('Bearer'):
		raise IncorrectAPIServerToken("Incorrect token")
	data = decode_jwt(server_token, config.security.secret_key)
	if ("id", "name") not in data:
		raise IncorrectAPIServerToken("Incorrect token")
	id = data["id"]
	name = data["name"]
	server = await uow.server.find_by_filters(
		GetServerFilter(
			name=name,
			server_id=ServerID.from_string(id)
		)
	)
	if not server:
		raise ServerNotExists(ServerID.from_string(id))
	return server
