from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.base.database.repo import SQLAlchemyRepo
from app.base.database.result import Result
from app.games.entities.game import GameEntity
from app.games.exceptions import GameAlreadyExists, GameNameAlreadyTaken, GameNotExists
from app.games.interfaces.persistance import GetGameFilter, AbstractGamesRepository


class GameRepository(AbstractGamesRepository, SQLAlchemyRepo):
    def _parse_exception(self, exc: IntegrityError) -> GameNameAlreadyTaken:
        """Parse exception responsible for parsing sqlalchemy integrity errors"""
        if not hasattr(exc.__cause__.__cause__, "constraint_name"):
            raise exc
        match exc.__cause__.__cause__.constraint_name:  # type: ignore
            case "ix_categories_name":
                return GameNameAlreadyTaken()

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

    async def update_game(self, game: GameEntity) -> Result[GameEntity, GameNameAlreadyTaken]:
        try:
            await self.session.merge(game)
        except IntegrityError as exc:
            await self.session.rollback()
            return Result.fail(self._parse_exception(exc))
        return Result.ok(game)

    async def delete_game(self, game: GameEntity) -> Result[GameEntity, GameNotExists]:
        try:
            await self.session.delete(game)
        except Exception:
            await self.session.rollback()
            return Result.fail(GameNotExists())

        return Result.ok(game)

    async def get_games(self) -> Sequence[GameEntity]:
        stmt = select(GameEntity)
        result = await self.session.scalars(stmt)

        return result.all()
