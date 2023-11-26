from typing import Sequence

from app.games.dto.player import PlayerDTO
from app.server.dto.server import GetPlayersKarmaDTO, RegisterServerDTO, ServerDTO, GetServerDTO
from app.server.interfaces.service import AbstractPlayerService, AbstractServerService
from app.server.interfaces.uow import AbstractServerUoW


class PlayerService(AbstractPlayerService):
	async def player_karmas(self, dto: GetPlayersKarmaDTO) -> Sequence[PlayerDTO]:
		pass


class ServerService(AbstractServerService):
	def __init__(
		self,
		uow: AbstractServerUoW,
	):
		self.uow = uow

	async def register_server(self, dto: RegisterServerDTO) -> ServerDTO:
		pass

	async def get_api_token(self, dto: GetServerDTO) -> str:
		pass

	async def get_server(self, dto: GetServerDTO) -> ServerDTO:
		pass
