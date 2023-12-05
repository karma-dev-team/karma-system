import abc
from typing import Protocol

from app.base.database.filters import filter_wrapper
from app.base.database.result import Result
from app.games.entities.game import GameEntity
from app.games.exceptions import GameAlreadyExists
from app.games.value_objects.ids import GameID


@filter_wrapper
class GetGameFilter:
    name: str | None
    game_id: GameID | None


class AbstractCategoryRepository(Protocol):
    pass


class AbstractGamesRepository(Protocol):
    @abc.abstractmethod
    async def by_filter(self, filter: GetGameFilter) -> GameEntity | None:
        pass

    @abc.abstractmethod
    async def add_game(self, game: GameEntity) -> Result[GameEntity, GameAlreadyExists]:
        pass
