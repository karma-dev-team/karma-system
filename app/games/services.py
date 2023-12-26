from typing import Sequence

from app.auth.access_policy import BasicAccessPolicy
from app.auth.exceptions import AccessDenied
from app.base.database.result import Result
from app.base.events.dispatcher import EventDispatcher
from app.games.dto.category import AddCategoryDTO, GetCategoryDTO, CategoryDTO, UpdateCategoryDTO
from app.games.dto.game import GetGameDTO, GameDTO, AddGameDTO, UpdateGameDTO
from app.games.entities.category import CategoryEntity
from app.games.entities.game import GameEntity
from app.games.exceptions import CategoryNotExists, GameNotExists, GameNameAlreadyTaken, CategoryNameAlreadyTaken
from app.games.interfaces.persistance import AbstractCategoryRepository, GetCategoryFilter, GetGameFilter
from app.games.interfaces.service import AbstractGameService, AbstractCategoryService
from app.games.interfaces.uow import AbstractGameUoW
from app.games.value_objects.ids import CategoryID, GameID
from app.user.enums import UserRoles


class GameService(AbstractGameService):
	def __init__(
			self,
			uow: AbstractGameUoW,
			event_dispatcher: EventDispatcher,
			access_policy: BasicAccessPolicy,
	):
		self.uow = uow
		self.event_dispatcher = event_dispatcher
		self.access_policy = access_policy

	async def get_game(self, dto: GetGameDTO) -> GameDTO:
		game = await self.uow.category.by_filter(
			GetCategoryFilter(
				name=dto.name,
				game_id=dto.game_id,
			)
		)
		if not game:
			raise GameNotExists()

		return GameDTO.model_validate(game)

	async def add_game(self, dto: AddGameDTO) -> GameDTO:
		game = GameEntity.create(
			name=dto.name,
			description=dto.description,
			image=None,
		)

		async with self.uow.transaction():
			result = await self.uow.game.add_game(game)
			match result:
				case Result(value, _):
					return GameDTO.model_validate(value)
				case Result(None, Exception() as exc):
					raise exc

	async def update_game(self, dto: UpdateGameDTO) -> GameDTO:
		if self.access_policy.check_role(UserRoles.admin):
			raise AccessDenied
		game = await self.uow.game.by_filter(
			GetGameFilter(
				game_id=dto.game_id,
			)
		)

		if not game:
			raise GameNotExists()

		if dto.data.name:
			game.name = dto.data.name
		if dto.data.description:
			game.description = dto.data.description

		async with self.uow.transaction():
			result = await self.uow.game.update_game(game)
			match result:
				case Result(value, None):
					return GameDTO.model_validate(value)
				case Result(None, GameNameAlreadyTaken() as exc):
					raise exc

	async def delete_game(self, game_id: GameID) -> GameDTO:
		if self.access_policy.check_role(UserRoles.admin):
			raise AccessDenied
		game = await self.uow.game.by_filter(
			GetGameFilter(
				game_id=game_id,
			)
		)

		if not game:
			raise GameNotExists()

		async with self.uow.transaction():
			# no need to validate result.
			# we already know that game exists
			await self.uow.game.delete_game(game)
			return GameDTO.model_validate(game)

	async def get_games(self) -> Sequence[GameDTO]:
		games = await self.uow.game.get_games()
		return [GameDTO.model_validate(game) for game in games]


class CategoryService(AbstractCategoryService):
	def __init__(
		self,
		uow: AbstractGameUoW,
		event_dispatcher: EventDispatcher,
		access_policy: BasicAccessPolicy
	):
		self.uow = uow
		self.event_dispatcher = event_dispatcher
		self.access_policy = access_policy

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

	async def update_category(self, dto: UpdateCategoryDTO) -> CategoryDTO:
		if self.access_policy.check_role(UserRoles.admin):
			raise AccessDenied
		category = await self.uow.category.by_filter(
			GetCategoryFilter(
				category=dto.category_id,
			)
		)

		if not category:
			raise GameNotExists()

		if dto.data.name:
			category.name = dto.data.name
		if dto.data.description:
			category.description = dto.data.description

		async with self.uow.transaction():
			result = await self.uow.category.update_category(category)
			match result:
				case Result(value, None):
					return CategoryDTO.model_validate(value)
				case Result(None, CategoryNameAlreadyTaken() as exc):
					raise exc

	async def delete_category(self, category_id: CategoryID) -> CategoryDTO:
		if self.access_policy.check_role(UserRoles.admin):
			raise AccessDenied
		category = await self.uow.category.by_filter(
			GetCategoryFilter(
				category_id=category_id,
			)
		)

		if not category:
			raise CategoryNotExists()

		async with self.uow.transaction():
			# no need to validate result.
			# we already know that game exists
			await self.uow.category.delete_category(category)
			return CategoryDTO.model_validate(category)

	async def get_categories(self) -> Sequence[CategoryDTO]:
		categories = await self.uow.category.get_categories()
		return [CategoryDTO.model_validate(category) for category in categories]
