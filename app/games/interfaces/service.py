import abc

from app.games.dto.category import GetCategoryDTO, AddCategoryDTO, CategoryDTO
from app.games.dto.game import GetGameDTO, GameDTO, AddGameDTO


class AbstractGameService:
	@abc.abstractmethod
	async def get_game(self, dto: GetGameDTO) -> GameDTO:
		pass

	@abc.abstractmethod
	async def add_game(self, dto: AddGameDTO) -> GameDTO:
		pass


class AbstractCategoryService:
	@abc.abstractmethod
	async def get_category(self, dto: GetCategoryDTO) -> CategoryDTO:
		pass

	@abc.abstractmethod
	async def add_category(self, dto: AddCategoryDTO) -> CategoryDTO:
		pass

