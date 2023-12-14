from app.base.dto import DTO, TimedDTO
from app.files.dtos.files import PhotoDTO
from app.games.value_objects.ids import GameID, CategoryID


class CategoryDTO(DTO, TimedDTO):
	id: CategoryID
	name: str
	game_id: GameID
	image: PhotoDTO | None


class GetCategoryDTO(DTO):
	name: str | None
	category_id: CategoryID | None


class AddCategoryDTO(DTO):
	name: str
	game_id: GameID
