from typing import Sequence

from app.auth.access_policy import BasicAccessPolicy
from app.auth.config import SecurityConfig
from app.auth.exceptions import AccessDenied
from app.base.database.result import Result
from app.base.events.dispatcher import EventDispatcher
from app.games.dto.player import PlayerDTO
from app.games.exceptions import GameNotExists
from app.games.interfaces.persistance import GetGameFilter
from app.games.interfaces.uow import AbstractGameUoW
from app.server.dto.player import GetPlayerDTO
from app.server.dto.server import GetPlayersKarmaDTO, RegisterServerDTO, ServerDTO, GetServerDTO, GetServersDTO
from app.server.entities.server import ServerEntity
from app.server.exceptions import ServerNotExists, ServerNotOwned
from app.server.interfaces.persistance import GetServersFilter, GetServerFilter
from app.server.interfaces.service import AbstractPlayerService, AbstractServerService
from app.server.interfaces.uow import AbstractServerUoW
from app.server.security import generate_jwt


class PlayerService(AbstractPlayerService):
	def __init__(self, uow: AbstractServerUoW, event_dispatcher: EventDispatcher) -> None:
		self.uow = uow
		self.event_dispatcher = event_dispatcher

	async def player_karmas(self, dto: GetPlayersKarmaDTO) -> Sequence[PlayerDTO]:
		pass

	async def player_connected(self, dto: GetPlayerDTO) -> PlayerDTO:
		pass

	async def player_disconnect(self, dto: GetPlayerDTO) -> PlayerDTO:
		pass


class ServerService(AbstractServerService):
	def __init__(
		self,
		uow: AbstractServerUoW,
		game_uow: AbstractGameUoW,
		access_policy: BasicAccessPolicy,
		event_dispatcher: EventDispatcher,
		config: SecurityConfig,
	):
		self.config = config
		self.game_uow = game_uow
		self.uow = uow
		self.access_policy = access_policy
		self.event_dispatcher = event_dispatcher

	async def register_server(self, dto: RegisterServerDTO) -> ServerDTO:
		server = ServerEntity.create(
			name=dto.name,
			ipv4=dto.ip,
			port=dto.port,
			owner_id=self.access_policy.user.id,
			game_id=dto.game_id,
			tags=dto.tags,
		)
		if self.access_policy.user.blocked:
			raise AccessDenied(self.access_policy.user.id)
		async with self.uow.transaction():
			result = await self.uow.server.add_server(server)
			match result:
				case Result(value, _):
					await self.event_dispatcher.publish_events(server.get_events())

					return ServerDTO.model_validate(value)
				case Result(None, err):
					raise err

	async def get_api_token(self, dto: GetServerDTO) -> str:
		server = await self.uow.server.find_by_filters(
			GetServerFilter(
				name=dto.name,
				server_id=dto.server_id,
			)
		)
		if not server:
			raise ServerNotExists(dto.name or dto.server_id)
		if server.owner_id != self.access_policy.user.id or self.access_policy.user.blocked:
			raise ServerNotOwned()
		return generate_jwt(
			data={
				"name": server.name,
				"id": server.id,
			},
			secret=self.config.secret_key
		)

	async def get_server(self, dto: GetServerDTO) -> ServerDTO:
		server = await self.uow.server.find_by_filters(
			GetServerFilter(
				name=dto.name,
				server_id=dto.server_id,
			)
		)
		if not server:
			raise ServerNotExists(dto.name or dto.server_id)
		return ServerDTO.model_validate(server)

	async def get_servers(self, dto: GetServersDTO) -> list[ServerDTO]:
		game = await self.game_uow.game.by_filter(
			GetGameFilter(
				name=dto.game,
			)
		)
		if not game:
			raise GameNotExists

		servers = await self.uow.server.filter(
			GetServersFilter(
				# tags=tags,  # TODO
				game_id=game.id,
				unregistered=dto.unregistered,
			)
		)

		return [ServerDTO.model_validate(server) for server in servers]
