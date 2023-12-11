import abc
from typing import Sequence

from app.server.dto.player import GetPlayerDTO, PlayerDTO
from app.server.dto.server import GetServerDTO, ServerDTO, GetPlayersKarmaDTO, RegisterServerDTO, GetServersDTO


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

	@abc.abstractmethod
	async def get_servers(self, dto: GetServersDTO) -> list[ServerDTO]:
		pass


class AbstractPlayerService:
	@abc.abstractmethod
	async def player_karmas(self, dto: GetPlayersKarmaDTO) -> Sequence[PlayerDTO]:
		pass

	@abc.abstractmethod
	async def player_disconnect(self, dto: GetPlayerDTO) -> PlayerDTO:
		pass

	@abc.abstractmethod
	async def player_connected(self, dto: GetPlayerDTO) -> PlayerDTO:
		pass

	@abc.abstractmethod
	async def get_player(self, dto: GetPlayerDTO) -> PlayerDTO:
		pass
