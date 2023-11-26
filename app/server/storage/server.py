from app.base.database.repo import SQLAlchemyRepo
from app.server.entities.server import ServerEntity
from app.server.interfaces.persistance import AbstractServerRepo
from app.server.value_objects.ids import ServerID


class ServerRepositoryImpl(AbstractServerRepo, SQLAlchemyRepo):
    async def find_by_id(self, server_id: ServerID) -> ServerEntity | None:
        return await self.session.get(ServerEntity, ident=str(server_id))
