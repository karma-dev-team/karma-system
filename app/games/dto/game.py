from app.base.dto import DTO, TimedDTO
from app.games.value_objects.ids import GameID


class GetGameDTO(DTO):
	game_id: GameID | None
	name: str | None


class GameDTO(DTO, TimedDTO):
	id: GameID
	name: str
	description: str
