import abc
from typing import Sequence

from app.games.dto.player import PlayerDTO
from app.server.dto.server import GetServerDTO, ServerDTO, GetPlayersKarmaDTO, RegisterServerDTO


class AbstractServerService:
	@abc.abstractmethod
	async def get_server(self, dto: GetServerDTO) -> ServerDTO:
		pass

	@abc.abstractmethod
	async def register_server(self, dto: RegisterServerDTO) -> ServerDTO:
		pass

	@abc.abstractmethod
	async def get_api_token(self, dto: GetServerDTO) -> str:
		pass


class AbstractPlayerService:
	@abc.abstractmethod
	async def player_karmas(self, dto: GetPlayersKarmaDTO) -> Sequence[PlayerDTO]:
		pass
