import abc

from app.games.dto.game import GetGameDTO, GameDTO


class AbstractGameService:
	@abc.abstractmethod
	async def get_game(self, dto: GetGameDTO) -> GameDTO:
		pass
