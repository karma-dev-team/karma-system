import abc
from dataclasses import field
from typing import Protocol

from app.base.database.filters import filter_wrapper
from app.base.database.result import Result
from app.games.entities.category import CategoryEntity
from app.games.entities.game import GameEntity
from app.games.exceptions import GameAlreadyExists
from app.games.value_objects.ids import GameID, CategoryID


@filter_wrapper
class GetCategoryFilter:
    name: str | None = field(default=None)
    category_id: CategoryID | None = field(default=None)


@filter_wrapper
class GetGameFilter:
    name: str | None = field(default=None)
    game_id: GameID | None = field(default=None)


class AbstractCategoryRepository(Protocol):
    @abc.abstractmethod
    async def by_filter(self, filter: GetCategoryFilter) -> CategoryEntity | None:
        pass

    @abc.abstractmethod
    async def add_category(self, cat: CategoryEntity) -> Result[CategoryEntity, None]:
        pass


class AbstractGamesRepository(Protocol):
    @abc.abstractmethod
    async def by_filter(self, filter: GetGameFilter) -> GameEntity | None:
        pass

    @abc.abstractmethod
    async def add_game(self, game: GameEntity) -> Result[GameEntity, GameAlreadyExists]:
        pass
