from typing import Annotated, Sequence
from uuid import UUID

from fastapi import APIRouter, Depends, Request, HTTPException
from starlette.responses import HTMLResponse
from starlette.status import HTTP_403_FORBIDDEN
from starlette.templating import Jinja2Templates

from app.auth.dependencies import user_dependency, user, role_required
from app.auth.providers import optional_user
from app.base.api.ioc import ioc_provider
from app.base.ioc import AbstractIoContainer
from app.server.dto.player import GetPlayerDTO, PlayerDTO
from app.server.dto.server import GetPlayersKarmaDTO, GetServerDTO, GetServersDTO, ApproveServerDTO, ServerDTO, \
	QueueServerDTO
from app.server.responses import APITokenData
from app.server.value_objects.ids import ServerID
from app.templating.provider import templating_provider
from app.user.entities import UserEntity
from app.user.enums import UserRoles

player_router = APIRouter(prefix="/player")
server_router = APIRouter()


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


@server_router.get('/server', name="server:get-servers-page", response_class=HTMLResponse)
async def get_servers(
	request: Request,
	filter: Annotated[GetServersDTO, Depends()],
	templates: Annotated[Jinja2Templates, Depends(templating_provider)],
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
):
	servers = await ioc.server_service().get_servers(filter)
	return templates.TemplateResponse("server/servers.html", {"request": request, 'servers': servers})


@server_router.get("/server/{server_id}/get", name="server:server-card", response_class=HTMLResponse)
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


@server_router.post("/server/approve", name="server:approve-server")
async def approve_server(
	dto: ApproveServerDTO,
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
) -> dict:
	await ioc.server_service().approve_servers(dto)
	return {'ok': True}


@server_router.post("/server/queue", name="server:queue-server")
async def queue_server(
	dto: QueueServerDTO,
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
	user: Annotated[UserEntity, Depends(user)],
) -> ServerDTO:

	return await ioc.server_service().queue_server(dto)


@server_router.get('/server/queue', name="server:queue-server-page", response_class=HTMLResponse)
async def queue_server_page(
	request: Request,
	templates: Annotated[Jinja2Templates, Depends(templating_provider)],
	user: Annotated[UserEntity, Depends(optional_user)]
):
	if not user:
		raise HTTPException(
			detail="Access denied",
			status_code=HTTP_403_FORBIDDEN,
		)
	return templates.TemplateResponse("server/server-registration.html", {"request": request, 'user': user})


@server_router.get(
	'server/queued',
	name='server:queued-servers-page',
	response_class=HTMLResponse,
	dependencies=[Depends(role_required(UserRoles.moderator))]
)
async def show_queued_servers(
	request: Request,
	templates: Annotated[Jinja2Templates, Depends(templating_provider)],
	user: Annotated[UserEntity, Depends(user)],
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
):
	if not user:
		raise HTTPException(
			detail="Access denied",
			status_code=HTTP_403_FORBIDDEN,
		)
	servers = ioc.server_service().get_servers(
		GetServersDTO(
			unregistered=True,
		)
	)
	return templates.TemplateResponse(
		"server/queued-servers.html",
		{'request': request, 'user': user, 'servers': servers}
	)
