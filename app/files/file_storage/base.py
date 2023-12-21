import abc
from asyncio import StreamReader
from typing import IO, Generic, TypeVar, Any

FileT = TypeVar("FileT", bound=StreamReader)


class File(Generic[FileT]):
    def __init__(
            self,
            body: FileT,
            mime_type: str | None = None,
            path: str | None = None,
            url: str | None = None, additional_data: dict[str, Any] | None = None
    ):
        self.path = path
        self.mime_type = mime_type
        self.body: FileT = body
        self.url = url
        self.size = 0
        self.additional_data = additional_data or {}

    def close(self):
        self.body.close()

    def __enter__(self):
        return self.body

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.close()

    async def __aenter__(self):
        return self.body

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.body.close()


class AbstractFileStorage(abc.ABC):
    """
    описывает общие интерфейсы
    по которым будет загружатся
    и выгружатся динамический контент
    """
    @abc.abstractmethod
    async def upload(self, body: FileT, key: str, mime_type: str) -> str:
        pass

    @abc.abstractmethod
    async def get_file(self, key: str) -> File:
        pass
