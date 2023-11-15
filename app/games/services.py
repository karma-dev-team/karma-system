from app.games.dto.game import GetGameDTO, GameDTO
from app.games.interfaces.service import AbstractGameService


class GameService(AbstractGameService):
	async def get_game(self, dto: GetGameDTO) -> GameDTO:
		pass
