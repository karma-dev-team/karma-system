from app.base.uow import AbstractUoW
from app.games.interfaces.persistance import AbstractGamesRepository, AbstractCategoryRepository


class AbstractGameUoW(AbstractUoW):
    game: AbstractGamesRepository
    category: AbstractCategoryRepository
