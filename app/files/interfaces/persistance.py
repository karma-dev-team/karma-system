from typing import Protocol

from app.base.database.result import Result
from app.base.typeid import TypeID
from app.files.entities import PhotoEntity, VideoEntity, DocumentEntity, FileEntity
from app.files.exceptions import FileNotExists

FileType = PhotoEntity | VideoEntity | DocumentEntity | FileEntity


class AbstractFileRepo(Protocol):
    async def file_by_unique_id(
            self, file_id: TypeID, file_type: FileType
    ) -> FileType | None:
        pass

    async def file_by_url(
            self, file_url: str, file_type: FileType,
    ) -> FileType | None:
        pass

    async def add_files(self, *file: FileType) -> Result[FileType, None]:
        pass

    async def edit_file(self, file: FileType) -> Result[FileType, FileNotExists]:
        pass

    # no deletion, only add, and update and get methods are available!
