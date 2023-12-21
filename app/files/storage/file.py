from sqlalchemy import select

from app.base.database.repo import SQLAlchemyRepo
from app.base.database.result import Result
from app.base.typeid import TypeID
from app.files.entities import DocumentEntity, VideoEntity, PhotoEntity, FileEntity, FileEntityTypes
from app.files.exceptions import FileNotExists
from app.files.interfaces.persistance import AbstractFileRepo


class FileRepo(SQLAlchemyRepo, AbstractFileRepo):
    async def file_by_unique_id(
            self, file_id: TypeID, file_type: FileEntityTypes
    ) -> FileEntityTypes | None:
        if file_type is FileEntity:
            file_types = DocumentEntity, VideoEntity, PhotoEntity
            for type in file_types:
                file = await self.file_by_unique_id(file_id, type)
                if not file:
                    continue
                return file
            return
        result = await self.session.get(file_type, ident=file_id)
        return result

    async def file_by_url(
            self, file_url: str, file_type: FileEntityTypes,
    ) -> FileEntityTypes | None:
        if file_type is FileEntity:
            file_types = DocumentEntity, VideoEntity, PhotoEntity
            for type in file_types:
                file = await self.file_by_url(file_url, type)
                if not file:
                    continue
                return file
            return
        stmt = select(file_type).where(file_type.file_url == str(file_url))
        file = await self.session.scalar(stmt)
        return file

    async def add_file(self, file: FileEntityTypes) -> Result[FileEntityTypes, None]:
        self.session.add(file)

        try:
            await self.session.commit()
            await self.session.refresh(file)
        except Exception:
            raise

        return Result.ok(file)

    async def edit_file(self, file: FileEntityTypes) -> Result[FileEntityTypes, FileNotExists]:
        try:
            db_file = await self.session.merge(file)
        except Exception:
            raise
        return Result.ok(db_file)
