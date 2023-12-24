import os.path
from pathlib import Path

import aiofiles

from app.files.file_storage.base import FileT, File, AbstractFileStorage


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

    async def upload(self, body: FileT, key: str, mime_type: str) -> str:
        if not os.path.exists(self.base_path):
            os.mkdir(self.base_path)
        file = File(
            path=str(self._build_path(key)),
            mime_type=mime_type,
            body=body,
        )
        async with aiofiles.open(file.path, "wb") as new_file:
            # not effective, but does not matter
            content = await body.read()

            await new_file.write(content)
        return self._build_url(key)

    async def get_file(self, key: str) -> File:
        path = self._build_path(key)
        if not os.path.exists(path):
            raise FileNotFoundError
        file = aiofiles.open(path, "rb")
        file = File(
            body=file,
            mime_type=None,
            path=str(path),
        )
        return file


def configure_file_storage() -> AbstractFileStorage:
    return LocalStorage("./static/data", "/static/data")
