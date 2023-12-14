from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.base.database.repo import SQLAlchemyRepo
from app.base.database.result import Result
from app.server.entities.server import ServerEntity
from app.server.exceptions import ServerAlreadyExists, IPPortAlreadyTaken
from app.server.interfaces.persistance import AbstractServerRepo, GetServersFilter
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
                stmt = stmt.where(ServerEntity.id == serv_id)

        result = await self.session.execute(stmt)

        return result.scalars().all()
