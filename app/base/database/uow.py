import asyncio
from contextlib import asynccontextmanager
from typing import Type, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.base.uow import AbstractUoW
from app.files.interfaces.persistance import AbstractFileRepo
from app.files.interfaces.uow import AbstractFileUoW
from app.games.interfaces.persistance import AbstractGamesRepository, AbstractCategoryRepository
from app.games.interfaces.uow import AbstractGameUoW
from app.games.storage.category import CategoryRepository
from app.games.storage.game import GameRepository
from app.karma.interfaces.persistence import AbstractKarmaRepository
from app.karma.interfaces.uow import AbstractKarmaUoW
from app.karma.storages.karma import KarmaRepoImpl
from app.server.interfaces.persistance import AbstractServerRepo, AbstractPlayerRepo
from app.server.interfaces.uow import AbstractServerUoW
from app.server.storage.player import PlayerRepositoryImpl
from app.server.storage.server import ServerRepositoryImpl
from app.user.interfaces import AbstractUserRepo
from app.user.interfaces.uow import AbstractUserUoW
from app.user.storage.user import UserRepoImpl


class SQLAlchemyBaseUoW(AbstractUoW):
    def __init__(self, session: AsyncSession):
        self._session = session
        self._in_transaction = False

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()

    @asynccontextmanager
    async def transaction(self) -> AsyncGenerator[None, None]:
        if self._in_transaction:
            raise RuntimeError("In transaction, need to rollback, or commit")

        self._in_transaction = True
        # bc in app/presentation/middleware.py we initialize transaction,
        # we need to use session
        # if not self._session.in_transaction():
        #     tx = await self._session.begin()
        # else:
        #     tx = await self._session.begin_nested()

        try:
            yield
        except Exception as exc:
            if self._session.in_transaction():
                # баг если не будет этой линии, то она не ожидая окончания транзакции
                # сделает rollback, то текущая операция прервется и вылетит ошибка
                # и что избежать этого надо немного подождать. если будут появлятся ошибки с
                # rollback, то просто увеличьте время сна. ЛЮТЫЙ КОСТЫЛЬ
                await asyncio.sleep(0.2)
                await self._session.rollback()
            raise exc
        else:
            await self._session.commit()
        finally:
            self._in_transaction = False


class SQLAlchemyUoW(SQLAlchemyBaseUoW, AbstractServerUoW, AbstractKarmaUoW, AbstractUserUoW, AbstractGameUoW, AbstractFileUoW):
    server: AbstractServerRepo
    player: AbstractPlayerRepo
    user: AbstractUserRepo
    karma: AbstractKarmaRepository
    game: AbstractGamesRepository
    category: AbstractCategoryRepository
    file: AbstractFileRepo

    def __init__(
        self,
        session: AsyncSession,
        *,
        file_repo: Type[AbstractFileRepo],
        server_repo: Type[AbstractServerRepo],
        player_repo: Type[AbstractPlayerRepo],
        user_repo: Type[AbstractUserRepo],
        karma_repo: Type[AbstractKarmaRepository],
        game_repo: Type[AbstractGamesRepository],
        category: Type[AbstractCategoryRepository],
    ) -> None:
        self.file = file_repo(session)
        self.server = server_repo(session)
        self.player = player_repo(session)
        self.user = user_repo(session)
        self.karma = karma_repo(session)
        self.game = game_repo(session)
        self.category = category(session)

        super().__init__(session)

    @classmethod
    def create(cls, session: AsyncSession) -> "SQLAlchemyUoW":
        return SQLAlchemyUoW(
            session=session,
            server_repo=ServerRepositoryImpl,
            player_repo=PlayerRepositoryImpl,
            user_repo=UserRepoImpl,
            karma_repo=KarmaRepoImpl,
            game_repo=GameRepository,
            category=CategoryRepository,
        )
