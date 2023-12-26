import asyncio
from typing import Sequence

from app.auth.access_policy import BasicAccessPolicy
from app.auth.config import SecurityConfig
from app.auth.exceptions import AccessDenied
from app.base.database.result import Result
from app.base.events.dispatcher import EventDispatcher
from app.files.interfaces.services import FileService
from app.games.exceptions import GameNotExists, CategoryNotExists
from app.games.interfaces.persistance import GetGameFilter, GetCategoryFilter
from app.games.interfaces.uow import AbstractGameUoW
from app.server.dto.player import GetPlayerDTO, PlayerDTO
from app.server.dto.server import GetPlayersKarmaDTO, ApproveServerDTO, ServerDTO, GetServerDTO, GetServersDTO, \
	QueueServerDTO
from app.server.entities.player import PlayerEntity, PlayerSelector
from app.server.entities.server import ServerEntity
from app.server.exceptions import ServerNotExists, ServerNotOwned, PlayerDoesNotExists, ServerNotRegistered
from app.server.interfaces.persistance import GetServersFilter, GetServerFilter, PlayerFilter
from app.server.interfaces.service import AbstractPlayerService, AbstractServerService
from app.server.interfaces.uow import AbstractServerUoW
from app.server.security import generate_jwt


class PlayerService(AbstractPlayerService):
	def __init__(self, uow: AbstractServerUoW, event_dispatcher: EventDispatcher) -> None:
		self.uow = uow
		self.event_dispatcher = event_dispatcher

	async def player_karmas(self, dto: GetPlayersKarmaDTO) -> Sequence[PlayerDTO]:
		return []  # TODO!!!

	async def player_connected(self, dto: GetPlayerDTO) -> PlayerDTO:
		player = await self.uow.player.find_by_filters(
			PlayerFilter.from_dto(dto)
		)
		async with self.uow.transaction():
			if not player:
				player = PlayerEntity.create(
					dto.name,
					selector=PlayerSelector(
						steam_id=dto.steam_id,
						ipv4=dto.ipv4,
						ipv6=dto.ipv6,
					)
				)

				result = await self.uow.player.add_player(player)
				player = result.value

			player.player_connectod()

			await self.event_dispatcher.publish_events(player.get_events())

			return PlayerDTO.model_validate(player)

	async def player_disconnect(self, dto: GetPlayerDTO) -> PlayerDTO:
		player = await self.uow.player.find_by_filters(
			PlayerFilter.from_dto(dto)
		)
		async with self.uow.transaction():
			if not player:
				player = PlayerEntity.create(
					dto.name,
					selector=PlayerSelector(
						steam_id=dto.steam_id,
						ipv4=dto.ipv4,
						ipv6=dto.ipv6,
					)
				)

				result = await self.uow.player.add_player(player)
				player = result.value

			player.player_disconnected()

			await self.event_dispatcher.publish_events(player.get_events())

		return PlayerDTO.model_validate(player)

	async def get_player(self, dto: GetPlayerDTO) -> PlayerDTO:
		player = await self.uow.player.find_by_filters(
			PlayerFilter.from_dto(dto)
		)
		if not player:
			raise PlayerDoesNotExists(player_id=player.id)

		return PlayerDTO.model_validate(player)


class ServerService(AbstractServerService):
	def __init__(
		self,
		uow: AbstractServerUoW,
		game_uow: AbstractGameUoW,
		access_policy: BasicAccessPolicy,
		event_dispatcher: EventDispatcher,
		config: SecurityConfig,
		file_service: FileService,
	):
		self.config = config
		self.game_uow = game_uow
		self.uow = uow
		self.access_policy = access_policy
		self.event_dispatcher = event_dispatcher
		self.file_service = file_service

	async def queue_server(self, dto: QueueServerDTO) -> ServerDTO:
		if self.access_policy.anonymous():
			raise AccessDenied
		icon = await self.file_service.upload_file(dto.icon)

		server = ServerEntity.create(
			name=dto.name,
			ipv4=dto.ip,
			port=dto.port,
			owner=self.access_policy.user,
			game_id=dto.game_id,
			tags=dto.tags,
			icon=icon,
			website_link=str(dto.website_link),
			discord_link=str(dto.discord_link)
		)
		# if self.access_policy.user.blocked:
		# 	raise AccessDenied(self.access_policy.user.id)
		async with self.uow.transaction():
			result = await self.uow.server.add_server(server)
			match result:
				case Result(value, None):
					await self.event_dispatcher.publish_events(server.get_events())

					return ServerDTO.model_validate(value)
				case Result(None, err):
					raise err

	async def approve_servers(self, dto: ApproveServerDTO) -> None:
		servers = await self.uow.server.filter(
			GetServersFilter(
				server_ids=dto.server_ids,
			)
		)
		if not servers:
			raise ServerNotExists(dto.server_ids[0])
		events = []
		async with self.uow.transaction():
			for server in servers:
				server.register()
				events.extend(server.get_events())
				await self.uow.server.update_server(server)
		await self.event_dispatcher.publish_events(events)

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
		if not server.registered:
			raise ServerNotRegistered(server.id)
		return generate_jwt(
			data={
				"name": server.name,
				"id": str(server.id),
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
		if not game and dto.game is not None:
			raise GameNotExists
		category = await self.game_uow.category.by_filter(
			GetCategoryFilter(
				name=dto.name,
			)
		)
		if not category and dto.category is not None:
			raise CategoryNotExists

		servers = await self.uow.server.filter(
			GetServersFilter(
				# tags=tags,  # TODO
				game_id=game.id if game else None,
				unregistered=dto.unregistered,
				category_id=category.id if category else None,
			)
		)

		return [ServerDTO.model_validate(server) for server in servers]
