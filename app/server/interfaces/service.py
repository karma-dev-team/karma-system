import abc

from app.server.dto.server import GetServerIdDTO, ServerDTO


class AbstractServerService:
	@abc.abstractmethod
	async def get_server(self, dto: GetServerIdDTO) -> ServerDTO:
		pass
