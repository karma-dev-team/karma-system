from sqlalchemy.ext.asyncio import AsyncSession

from app.base.uow import AbstractUoW
from app.karma.interfaces.uow import AbstractKarmaUoW
from app.server.interfaces.persistance import AbstractServerRepo, AbstractPlayerRepo
from app.server.interfaces.uow import AbstractServerUoW
from app.server.storage.player import PlayerRepositoryImpl
from app.server.storage.server import ServerRepositoryImpl


class SQLAlchemyUoW(AbstractUoW, AbstractServerUoW, AbstractKarmaUoW):
    server: AbstractServerRepo
    player: AbstractPlayerRepo

    def __init__(self, session: AsyncSession) -> None:
        self.server = ServerRepositoryImpl(session)
        self.player = PlayerRepositoryImpl(session)
