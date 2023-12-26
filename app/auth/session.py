import abc
import asyncio

from redis.asyncio import Redis, ConnectionPool
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.config import RedisConfig
from app.auth.entity import UserSession


class AbstractAuthSession:
    @abc.abstractmethod
    async def get(self, session_id: str) -> str:
        pass

    @abc.abstractmethod
    async def set(self, session_id: str, id: str) -> None:
        pass


class MemoryAuthSession(AbstractAuthSession):
    def __init__(self):
        self.data = {}

    async def get(self, session_id: str) -> str | None:
        return self.data.pop(session_id, None)

    async def set(self, session_id: str, id: str) -> None:
        self.data[session_id] = id


class RedisAuthSession(AbstractAuthSession):
    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    async def get(self, session_id: str) -> str | None:
        return await self.redis.get(session_id)

    async def set(self, session_id: str, id: str) -> None:
        await self.redis.set(session_id, id)


class DBAuthSession(AbstractAuthSession):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, session_id: str) -> str | None:
        stmt = select(UserSession).where(UserSession.session_id == session_id)
        ent = await self.session.scalar(stmt)
        if not ent:
            return
        return ent.id

    async def set(self, session_id: str, user_id: str) -> None:
        ent = UserSession(session_id=session_id, id=user_id)
        self.session.add(ent)

        try:
            await self.session.commit()
            # waiting until commit has been done
            # because when it'll go to main page
            # it will load user using get, and at the same time
            # will try to use scalar, and overlaping each other
            # so we need to wait until commit is done
            # TODO: use more reliable way to wait until commit is done!
            # await asyncio.sleep(0.3)
        except IntegrityError:
            return


def load_redis(redis: RedisConfig):
    redis = Redis(connection_pool=ConnectionPool.from_url(redis.dsn))
    return RedisAuthSession(redis)
