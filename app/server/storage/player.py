from sqlalchemy import select

from app.base.database.repo import SQLAlchemyRepo
from app.base.database.result import Result
from app.server.entities.player import PlayerEntity
from app.server.interfaces.persistance import AbstractPlayerRepo, PlayerFilter


class PlayerRepositoryImpl(AbstractPlayerRepo, SQLAlchemyRepo):
    async def find_by_filters(self, filter_: PlayerFilter) -> PlayerEntity | None:
        stmt = select(PlayerEntity)

        if filter_.ipv4 is not None:
            stmt = stmt.where(PlayerEntity.ipv4 == filter_.ipv4)
        if filter_.ipv6 is not None:
            stmt = stmt.where(PlayerEntity.ipv6 == filter_.ipv6)
        if filter_.name is not None:
            stmt = stmt.where(PlayerEntity.name == filter_.name)
        if filter_.steam_id is not None:
            stmt = stmt.where(PlayerEntity.steam_id == filter_.steam_id)
        if filter_.player_id is not None:
            stmt = stmt.where(PlayerEntity.id == filter_.player_id)

        result = await self.session.execute(stmt)
        return result.unique().scalar_one_or_none()

    async def add_player(self, player: PlayerEntity) -> Result[PlayerEntity, None]:
        self.session.add(player)

        try:
            await self.session.commit()
            await self.session.refresh(player)
        except Exception as exc:
            raise exc
        return Result.ok(player)

    async def edit_player(self, player: PlayerEntity) -> Result[PlayerEntity, None]:
        try:
            await self.session.merge(player)
        except Exception:
            raise

        return Result.ok(player)
