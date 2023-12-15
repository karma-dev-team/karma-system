import abc
import asyncio

from redis.asyncio import Redis, ConnectionPool
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
        ent = await self.session.get(UserSession, ident=session_id)
        return ent.id

    async def set(self, session_id: str, user_id: str) -> None:
        ent = UserSession(session_id=session_id, id=user_id)
        self.session.add(ent)

        try:
            await self.session.flush((ent,))
        except IntegrityError:
            return 


def load_redis(redis: RedisConfig):
    redis = Redis(connection_pool=ConnectionPool.from_url(redis.dsn))
    return RedisAuthSession(redis)
