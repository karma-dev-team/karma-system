from ipaddress import IPv4Address, AddressValueError
from typing import Annotated, Sequence
from uuid import UUID

from fastapi import APIRouter, Depends, Request, HTTPException, Form
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.status import HTTP_403_FORBIDDEN
from starlette.templating import Jinja2Templates

from app.auth.dependencies import user, role_required
from app.auth.providers import optional_user
from app.base.api.ioc import ioc_provider
from app.base.ioc import AbstractIoContainer
from app.games.dto.game import GetGameDTO
from app.games.exceptions import GameNotExists, CategoryNotExists
from app.server.dto.player import GetPlayerDTO, PlayerDTO
from app.server.dto.server import GetPlayersKarmaDTO, GetServerDTO, GetServersDTO, ApproveServersDTO, ServerDTO, \
	QueueServerDTO
from app.server.exceptions import ServerAlreadyExists, IPPortAlreadyTaken
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


@player_router.post(
	"/get",
	name='player:fetch-player',
)
async def fetch_player(
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
	data: GetPlayerDTO,
) -> PlayerDTO:
	return await ioc.player_service().get_player(data)

@server_router.get("/api-token/{server_id}", name="server:get-api-token")
async def get_api_token(
	server_id: UUID,
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
	# user: Annotated[UserEntity, Depends(user_provider)]   # TODO: UNCOMMENT ON PRODUCTION
) -> APITokenData:
	return APITokenData(token=(
		await ioc.server_service().get_api_token(
				GetServerDTO(
					server_id=ServerID.from_uuid(server_id),
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
	user: Annotated[UserEntity, Depends(optional_user)],
):
	filter = GetServersDTO(
		unregistered=True,
		**filter.model_dump(exclude={'unregistered'}),
	)
	try:
		servers = await ioc.server_service().get_servers(filter)
	except (GameNotExists, CategoryNotExists):
		servers = None
	games = await ioc.game_service().get_games()
	categories = await ioc.category_service().get_categories()

	return templates.TemplateResponse(
		"server/servers.html",
		{
			"request": request,
			'servers': servers,
			'user': user,
			'games': games,
			'categories': categories,
		}
	)


@server_router.get("/server/{server_id}/get", name="server:server-card", response_class=HTMLResponse)
async def server_card_by_id(
	request: Request,
	server_id: UUID,
	templates: Annotated[Jinja2Templates, Depends(templating_provider)],
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
	user: Annotated[UserEntity, Depends(optional_user)]
):
	dto = GetServerDTO(
		server_id=ServerID.from_uuid(server_id)
	)
	server = await ioc.server_service().get_server(dto)
	api_token = await ioc.server_service().get_api_token(dto)
	return templates.TemplateResponse('server/server-card.html', {
		'request': request,
		'server': server,
		'user': user,
		'api_token': api_token,
	})


@server_router.post("/server/approve", name="server:approve-server")
async def approve_servers(
	dto: ApproveServersDTO,
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
) -> dict:
	await ioc.server_service().approve_servers(dto)
	return {'ok': True}


@server_router.post("/server/queue", name="server:queue-server")
async def queue_server(
	request: Request,
	name: Annotated[str, Form()],
	description: Annotated[str, Form()],
	country: Annotated[str, Form()],
	port: Annotated[int, Form()],
	ip: Annotated[str, Form()],
	game: Annotated[str, Form()],
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
	user: Annotated[UserEntity, Depends(user)],
	templates: Annotated[Jinja2Templates, Depends(templating_provider)],
):
	games = await ioc.game_service().get_games()
	try:
		ip = IPv4Address(ip)
	except AddressValueError:
		return templates.TemplateResponse(
			"server/server-registration.html",
			{
				'request': request,
				'user': user,
				'games': games,
				'error_msg': "Не правильный IPv4 адрес"
			}
		)
	game = await ioc.game_service().get_game(
		GetGameDTO(
			name=game,
		)
	)
	try:
		await ioc.server_service().queue_server(
			QueueServerDTO(
				name=name,
				description=description,
				country_code=country,
				ip=ip,
				game_id=game.id,
				port=port,
			)
		)
	except (ServerAlreadyExists, IPPortAlreadyTaken):
		return templates.TemplateResponse(
			"server/server-registration.html",
			{
				'request': request,
				'user': user,
				'games': games,
				'error_msg': "Сервер с таким именем или ip уже существует"
			}
		)
	response = RedirectResponse("/", status_code=302)

	return response


@server_router.get('/server/queue', name="server:queue-server-page", response_class=HTMLResponse)
async def queue_server_page(
	request: Request,
	templates: Annotated[Jinja2Templates, Depends(templating_provider)],
	user: Annotated[UserEntity, Depends(optional_user)],
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
):
	if not user:
		raise HTTPException(
			detail="Access denied",
			status_code=HTTP_403_FORBIDDEN,
		)
	games = await ioc.game_service().get_games()

	return templates.TemplateResponse(
		"server/server-registration.html",
		{
			"request": request,
			'user': user,
			'games': games,
		}
	)


@server_router.get(
	'/server/queued',
	name='server:queued-servers-page',
	response_class=HTMLResponse,
	# dependencies=[Depends(role_required(UserRoles.moderator, UserRoles.admin))]
)
async def show_queued_servers(
	request: Request,
	filter: Annotated[GetServersDTO, Depends()],
	templates: Annotated[Jinja2Templates, Depends(templating_provider)],
	user: Annotated[UserEntity, Depends(user)],
	ioc: Annotated[AbstractIoContainer, Depends(ioc_provider)],
):
	servers = await ioc.server_service().get_servers(
		GetServersDTO(
			unregistered=True,
			**filter.model_dump(exclude={'unregistered'})
		)
	)
	games = await ioc.game_service().get_games()
	categories = await ioc.category_service().get_categories()

	return templates.TemplateResponse(
		"server/queued-servers.html",
		{
			'request': request,
			'user': user,
			'servers': servers,
			'games': games,
			'categories': categories,
		}
	)
