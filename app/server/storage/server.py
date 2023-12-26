from typing import Sequence

from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError

from app.base.database.repo import SQLAlchemyRepo
from app.base.database.result import Result
from app.games.entities.category import CategoryEntity
from app.server.entities.server import ServerEntity
from app.server.exceptions import ServerAlreadyExists, IPPortAlreadyTaken
from app.server.interfaces.persistance import AbstractServerRepo, GetServersFilter, GetServerFilter
from app.server.value_objects.ids import ServerID


class ServerRepositoryImpl(AbstractServerRepo, SQLAlchemyRepo):
    async def find_by_id(self, server_id: ServerID) -> ServerEntity | None:
        return await self.session.get(ServerEntity, ident=str(server_id))

    async def add_server(self, server: ServerEntity) -> Result[ServerEntity, ServerAlreadyExists | IPPortAlreadyTaken]:
        self.session.add(server)

        try:
            await self.session.commit()
            await self.session.refresh(server)
        except IntegrityError as exc:
            return Result.fail(ServerAlreadyExists())
        except Exception as exc:
            raise exc
        return Result.ok(server)

    async def filter(self, filter: GetServersFilter) -> Sequence[ServerEntity]:
        stmt = select(ServerEntity)
        if filter.game_id is not None:
            stmt = stmt.where(ServerEntity.game_id == filter.game_id)
        if filter.unregistered is not None:
            stmt = stmt.where(ServerEntity.registered != filter.unregistered)
        if filter.server_ids is not None:
            # to filter out duplicates without using DB resources
            ids = set(filter.server_ids)
            for serv_id in ids:
                stmt = stmt.where(ServerEntity.id == str(serv_id))
        if filter.name is not None:
            stmt = select(
                ServerEntity, func.similarity(ServerEntity.name, filter.name)
            ).where(
                ServerEntity.name.bool_op("%")(filter.name),
            ).order_by(
                func.similarity(ServerEntity.name, filter.name).desc(),
            )
        if filter.category_id:
            stmt = stmt.where(
                CategoryEntity.game_id == ServerEntity.game_id
            ).join(CategoryEntity)

        result = await self.session.execute(stmt)

        return result.unique().scalars().all()

    async def update_server(self, server: ServerEntity) -> ServerEntity:
        try:
            await self.session.merge(server)
        except Exception:
            raise
        return server

    async def find_by_filters(self, filter_: GetServerFilter) -> ServerEntity | None:
        stmt = select(ServerEntity)

        if filter_.name is not None:
            stmt = stmt.where(ServerEntity.name == filter_.name)
        if filter_.server_id is not None:
            stmt = stmt.where(ServerEntity.id == filter_.server_id)

        result = await self.session.execute(stmt)
        return result.unique().scalar_one_or_none()
