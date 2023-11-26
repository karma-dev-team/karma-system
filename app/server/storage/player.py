from app.base.database.result import Result
from app.server.entities.player import PlayerEntity
from app.server.interfaces.persistance import AbstractPlayerRepo, PlayerFilter


class PlayerRepositoryImpl(AbstractPlayerRepo):
    async def find_by_filters(self, filter_: PlayerFilter) -> PlayerEntity | None:
        pass

    async def add_player(self, player: PlayerEntity) -> Result[PlayerEntity, None]:
        pass
