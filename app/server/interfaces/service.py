import abc
from typing import Sequence

from app.server.dto.player import GetPlayerDTO, PlayerDTO
from app.server.dto.server import GetServerDTO, ServerDTO, GetPlayersKarmaDTO, ApproveServersDTO, GetServersDTO, \
	QueueServerDTO, UpdateServerDTO


class AbstractServerService:
	@abc.abstractmethod
	async def get_server(self, dto: GetServerDTO) -> ServerDTO:
		pass

	@abc.abstractmethod
	async def approve_servers(self, dto: ApproveServersDTO) -> None:
		"""adds server to queue of registration to be able see in admin panel"""
		pass

	@abc.abstractmethod
	async def queue_server(self, dto: QueueServerDTO) -> ServerDTO:
		"""adds server to queue of registration to be able see in admin panel"""
		pass

	@abc.abstractmethod
	async def get_api_token(self, dto: GetServerDTO) -> str:
		pass

	@abc.abstractmethod
	async def get_servers(self, dto: GetServersDTO) -> list[ServerDTO]:
		pass

	@abc.abstractmethod
	async def delete_server(self, dto: GetServerDTO) -> ServerDTO:
		pass

	@abc.abstractmethod
	async def update_server(self, dto: UpdateServerDTO) -> ServerDTO:
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
