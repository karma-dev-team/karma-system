from typing import Sequence

from app.acl.access_policy import BasicAccessPolicy
from app.acl.exceptions import NotEnoughPermissions
from app.base.database.result import Result
from app.base.events.dispatcher import EventDispatcher
from app.games.dto.player import PlayerDTO
from app.server.dto.player import GetPlayerDTO
from app.server.dto.server import GetPlayersKarmaDTO, RegisterServerDTO, ServerDTO, GetServerDTO
from app.server.entities.server import ServerEntity
from app.server.interfaces.service import AbstractPlayerService, AbstractServerService
from app.server.interfaces.uow import AbstractServerUoW


class PlayerService(AbstractPlayerService):
	async def player_karmas(self, dto: GetPlayersKarmaDTO) -> Sequence[PlayerDTO]:
		pass

	async def player_connected(self, dto: GetPlayerDTO) -> PlayerDTO:
		pass


class ServerService(AbstractServerService):
	def __init__(
		self,
		uow: AbstractServerUoW,
		access_policy: BasicAccessPolicy,
		event_dispatcher: EventDispatcher,
	):
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
			raise NotEnoughPermissions(self.access_policy.user.id)
		async with self.uow.transaction():
			result = await self.uow.server.add_server(server)
			match result:
				case Result(value, _):
					await self.event_dispatcher.publish_events(server.get_events())

					return ServerDTO.model_validate(value)
				case Result(None, err):
					raise err

	async def get_api_token(self, dto: GetServerDTO) -> str:
		pass

	async def get_server(self, dto: GetServerDTO) -> ServerDTO:
		pass
