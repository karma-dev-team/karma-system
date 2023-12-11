from app.base.database.result import Result
from app.base.events.dispatcher import EventDispatcher
from app.games.dto.category import AddCategoryDTO, GetCategoryDTO, CategoryDTO
from app.games.dto.game import GetGameDTO, GameDTO, AddGameDTO
from app.games.entities.category import CategoryEntity
from app.games.exceptions import CategoryNotExists, GameNotExists
from app.games.interfaces.persistance import AbstractCategoryRepository, GetCategoryFilter
from app.games.interfaces.service import AbstractGameService, AbstractCategoryService
from app.games.interfaces.uow import AbstractGameUoW


class GameService(AbstractGameService):
	def __init__(self, uow: AbstractGameUoW, event_dispatcher: EventDispatcher):
		self.uow = uow
		self.event_dispatcher = event_dispatcher

	async def get_game(self, dto: GetGameDTO) -> GameDTO:
		game = await self.uow.category.by_filter(
			GetCategoryFilter(
				name=dto.name,
				game_id=dto.game_id,
			)
		)
		if not game:
			raise GameNotExists(dto.category_id)

		return GameDTO.model_validate(game)

	async def add_game(self, dto: AddGameDTO) -> GameDTO:
		game = CategoryEntity.create(
			name=dto.name,
			game_id=dto.game_id,
		)

		async with self.uow.transaction():
			result = await self.uow.category.add_category(game)
			match result:
				case Result(value, _):
					await self.event_dispatcher.publish_events(game.get_events())

					return GameDTO.model_validate(value)
				case Result(None, Exception() as exc):
					raise exc


class CategoryService(AbstractCategoryService):
	def __init__(self, uow: AbstractGameUoW, event_dispatcher: EventDispatcher):
		self.uow = uow
		self.event_dispatcher = event_dispatcher

	async def get_category(self, dto: GetCategoryDTO) -> CategoryDTO:
		category = await self.uow.category.by_filter(
			GetCategoryFilter(
				name=dto.name,
				category_id=dto.category_id,
			)
		)
		if not category:
			raise CategoryNotExists(dto.category_id)

		return CategoryDTO.model_validate(category)

	async def add_category(self, dto: AddCategoryDTO) -> CategoryDTO:
		category = CategoryEntity.create(
			name=dto.name,
			game_id=dto.game_id,
		)

		async with self.uow.transaction():
			result = await self.uow.category.add_category(category)
			match result:
				case Result(value, _):
					await self.event_dispatcher.publish_events(category.get_events())

					return CategoryDTO.model_validate(value)
				case Result(None, Exception() as exc):
					raise exc
