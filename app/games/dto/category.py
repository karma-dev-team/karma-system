from pydantic import Field

from app.base.dto import DTO, TimedDTO
from app.files.dtos.files import PhotoDTO
from app.files.dtos.input_file import InputFileType
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


class UpdateCategoryDataDTO(DTO):
	name: str
	game_id: GameID
	image: InputFileType | None = Field(default=None)


class UpdateCategoryDTO(DTO):
	category_id: CategoryID
	data: UpdateCategoryDataDTO
