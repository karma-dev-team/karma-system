from sqlalchemy import select

from app.base.database.repo import SQLAlchemyRepo
from app.base.database.result import Result
from app.games.entities.game import GameEntity
from app.games.exceptions import GameAlreadyExists
from app.games.interfaces.persistance import GetGameFilter, AbstractGamesRepository


class GameRepository(AbstractGamesRepository, SQLAlchemyRepo):
    async def by_filter(self, filter: GetGameFilter) -> GameEntity | None:
        stmt = select(GameEntity)

        if filter.game_id is not None:
            stmt = stmt.where(GameEntity.id == str(filter.game_id))
        if filter.name is not None:
            stmt = stmt.where(GameEntity.name == str(filter.name))

        result = await self.session.execute(stmt)

        return result.unique().scalar_one_or_none()

    async def add_game(self, game: GameEntity) -> Result[GameEntity, GameAlreadyExists]:
        self.session.add(game)

        try:
            await self.session.commit()
            await self.session.refresh(game)
        except Exception as exc:
            raise exc
        return Result.ok(game)

