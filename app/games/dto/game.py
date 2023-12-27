from pydantic import Field

from app.base.dto import DTO, TimedDTO
from app.games.value_objects.ids import GameID


class GetGameDTO(DTO):
	game_id: GameID | None = Field(default=None)
	name: str | None = Field(default=None)


class GameDTO(DTO, TimedDTO):
	id: GameID
	name: str
	description: str


class AddGameDTO(DTO):
	name: str
	description: str


class UpdateGameDataDTO(DTO):
	name: str
	description: str


class UpdateGameDTO(DTO):
	game_id: GameID
	data: UpdateGameDataDTO
