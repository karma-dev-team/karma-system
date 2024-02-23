import abc
import asyncio
from asyncio import StreamReader, iscoroutine
from pathlib import Path
from typing import Generic, TypeVar, Any, Sequence

FileT = TypeVar("FileT", bound=StreamReader)


class File(Generic[FileT]):
    def __init__(
            self,
            body: FileT,
            key: str,
            mime_type: str | None = None,
            path: str | None = None,
            url: str | None = None, additional_data: dict[str, Any] | None = None,
    ):
        self.key = key
        self.path = path
        self.mime_type = mime_type
        file = StreamReader(limit=2 ** 64)
        file.feed_data(body)
        self.body = file
        self.url = url
        self.size = 0
        self.additional_data = additional_data or {}

    def close(self):
        if close := getattr(self.body, 'close'):
            if iscoroutine(close):
                asyncio.run(close())
            else:
                close()

    def __enter__(self):
        return self.body

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.close()

    async def __aenter__(self):
        return self.body

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def set_path(self, path: Path):
        self.path = str(path)


class AbstractFileStorage(abc.ABC):
    """
    описывает общие интерфейсы
    по которым будет загружатся
    и выгружатся динамический контент
    """
    @abc.abstractmethod
    async def upload(self, file: File) -> str:
        pass

    @abc.abstractmethod
    async def upload_files(self, *files: File) -> Sequence[str]:
        pass

    @abc.abstractmethod
    async def get_file(self, key: str) -> File:
        pass
