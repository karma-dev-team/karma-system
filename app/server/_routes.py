from typing import Annotated, Sequence
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from app.base.api.ioc import ioc_provider
from app.base.ioc import AbstractIoContainer
from app.server.dto.player import GetPlayerDTO, PlayerDTO
from app.server.dto.server import GetPlayersKarmaDTO, GetServerDTO, GetServersDTO
from app.server.responses import APITokenData
from app.server.value_objects.ids import ServerID
from app.templating.provider import templating_provider

player_router = APIRouter(prefix="/player")
server_router = APIRouter(prefix="/server")


@player_router.post("/connect", name="player:connect_event")
async def connect_event(
	data: GetPlayerDTO,
	# server: Annotated[ServerEntity, Depends(server_provider)],  # TODO: UNCOMMENT ON PRODUCTION
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
) -> PlayerDTO:
	return await ioc.player_service().player_connected(data)


@player_router.post("/disconnect", name='player:disconnect_event')
async def disconnect_event(
	data: GetPlayerDTO,
	# server: Annotated[ServerEntity, Depends(server_provider)],  # TODO: UNCOMMENT ON PRODUCTION
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
) -> PlayerDTO:
	return await ioc.player_service().player_disconnect(data)


@player_router.get("/player/{ply_id}", name="player:get-player-info")
async def player_info(
	data: GetPlayerDTO,
	# server: Annotated[ServerEntity, Depends(server_provider)],  # TODO: UNCOMMENT ON PRODUCTION
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
) -> PlayerDTO:
	return await ioc.player_service().get_player(data)


@player_router.post("/players", name="player:get-players-list")
async def handle_players_list(
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
	# server: Annotated[ServerEntity, Depends(server_provider)],  # TODO: UNCOMMENT ON PRODUCTION
	data: GetPlayersKarmaDTO,
) -> Sequence[PlayerDTO]:
	return await ioc.player_service().player_karmas(data)


@server_router.get("/api-token/{server_id}", name="server:get-api-token")
async def get_api_token(
	server_id: UUID,
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
	# user: Annotated[UserEntity, Depends(user_provider)]   # TODO: UNCOMMENT ON PRODUCTION
) -> APITokenData:
	return APITokenData(token=(
		await ioc.server_service().get_api_token(
				GetServerDTO(
					server_id=server_id,
				)
			)
		)
	)


@server_router.get('/servers', name="server:get-servers-page", response_class=HTMLResponse)
async def get_servers(
	request: Request,
	filter: Annotated[GetServersDTO, Depends()],
	templates: Annotated[Jinja2Templates, Depends(templating_provider)],
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
):
	servers = await ioc.server_service().get_servers(filter)
	return templates.TemplateResponse("server/servers.html", {"request": request, 'servers': servers})


@server_router.get("/server/{server_id}", name="server:server-card", response_class=HTMLResponse)
async def server_card_by_id(
	request: Request,
	server_id: UUID,
	templates: Annotated[Jinja2Templates, Depends(templating_provider)],
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
):
	server = await ioc.server_service().get_server(
		GetServerDTO(
			server_id=ServerID.from_uuid(server_id)
		)
	)
	return templates.TemplateResponse('server/server-card.html', {'request': request, 'server': server})
