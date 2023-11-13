import abc

from app.server.dto.server import GetServerIdDTO


class AbstractServerService:
	@abc.abstractmethod
	async def get_server(self, dto: GetServerIdDTO) -> ServerDTO:
		pass