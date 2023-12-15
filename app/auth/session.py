import abc
import asyncio

from redis.asyncio import Redis, ConnectionPool

from app.auth.config import RedisConfig


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


def load_redis(redis: RedisConfig):
    redis = Redis(connection_pool=ConnectionPool.from_url(redis.dsn))
    return RedisAuthSession(redis)
