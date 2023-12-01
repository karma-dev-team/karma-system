from typing import Sequence

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
	):
		self.uow = uow

	async def register_server(self, dto: RegisterServerDTO) -> ServerDTO:
		server = ServerEntity.create(
			name=dto.name,
			ipv4=dto.ip,
			port=dto.port,
			owner_id=
		)

	async def get_api_token(self, dto: GetServerDTO) -> str:
		pass

	async def get_server(self, dto: GetServerDTO) -> ServerDTO:
		pass
