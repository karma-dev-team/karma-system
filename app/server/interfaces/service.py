import abc
from typing import Sequence

from app.games.dto.player import PlayerDTO
from app.server.dto.server import GetServerIdDTO, ServerDTO, GetPlayersKarmaDTO


class AbstractServerService:
	@abc.abstractmethod
	async def get_server(self, dto: GetServerIdDTO) -> ServerDTO:
		pass


class AbstractPlayerService:
	@abc.abstractmethod
	async def player_karmas(self, dto: GetPlayersKarmaDTO) -> Sequence[PlayerDTO]:
		pass
