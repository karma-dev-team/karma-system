import abc

from app.games.dto.category import GetCategoryDTO, AddCategoryDTO, CategoryDTO, UpdateCategoryDTO
from app.games.dto.game import GetGameDTO, GameDTO, AddGameDTO, UpdateGameDTO
from app.games.value_objects.ids import GameID, CategoryID


class AbstractGameService:
	@abc.abstractmethod
	async def get_game(self, dto: GetGameDTO) -> GameDTO:
		pass

	@abc.abstractmethod
	async def add_game(self, dto: AddGameDTO) -> GameDTO:
		pass

	@abc.abstractmethod
	async def update_game(self, dto: UpdateGameDTO) -> GameDTO:
		pass

	@abc.abstractmethod
	async def delete_game(self, game_id: GameID) -> GameDTO:
		pass


class AbstractCategoryService:
	@abc.abstractmethod
	async def get_category(self, dto: GetCategoryDTO) -> CategoryDTO:
		pass

	@abc.abstractmethod
	async def add_category(self, dto: AddCategoryDTO) -> CategoryDTO:
		pass

	@abc.abstractmethod
	async def update_category(self, dto: UpdateCategoryDTO) -> CategoryDTO:
		pass

	@abc.abstractmethod
	async def delete_category(self, category_id: CategoryID) -> CategoryDTO:
		pass

