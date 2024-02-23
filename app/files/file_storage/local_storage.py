import asyncio
import os.path
from pathlib import Path
from typing import Sequence

import aiofiles
from aiohttp import StreamReader
from aiohttp.client_proto import ResponseHandler

from app.files.file_storage.base import File, AbstractFileStorage


class LocalStorage(AbstractFileStorage):
    """
    Очень простая и наивная реализация передачи файлов
    """
    def __init__(self, base_path: Path | str, base_url: str):
        if isinstance(base_path, str):
            base_path = Path(base_path)
        self.base_path: Path = base_path
        self.base_url = base_url

    def _build_path(self, key: str):
        return self.base_path.joinpath(key)

    def _build_url(self, key: str) -> str:
        if self.base_url[-1] == "/":
            base_url = self.base_url[:-1]
        else:
            base_url = self.base_url
        return f"{base_url}/{key}"

    async def upload(self, file: File) -> str:
        if not os.path.exists(self.base_path):
            os.mkdir(self.base_path)
        file.set_path(self._build_path(file.key))

        async with aiofiles.open(file.path, "wb") as new_file:
            # not effective, but does not matter
            content = await file.body.read()

            await new_file.write(content)
            return self._build_url(file.key)

    async def upload_files(self, *files: File) -> Sequence[str]:
        for file in files:
            yield await self.upload(file)

    async def get_file(self, key: str) -> File:
        path = self._build_path(key)
        if not os.path.exists(path):
            raise FileNotFoundError
        file = await aiofiles.open(path, "rb")
        file = File(
            body=file,
            mime_type=None,
            path=str(path),
            key=key,
        )
        return file


def configure_file_storage() -> AbstractFileStorage:
    return LocalStorage("./static/data", "/static/data")
