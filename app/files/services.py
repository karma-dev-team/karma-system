import asyncio
import uuid
from asyncio import StreamReader
from typing import Type

from aiohttp import ClientSession

from app.base.logging.logger import get_logger
from app.base.typeid import TypeID
from app.files.dtos.files import FileDTOTypes, PhotoDTO, DocumentDTO, VideoDTO
from app.files.dtos.input_file import InputFile
from app.files.entities import PhotoEntity, VideoEntity, FileEntityTypes, DocumentEntity, FileEntity
from app.files.exceptions import FileTypeIncorrect, UnableToDownloadFile
from app.files.file_storage.base import AbstractFileStorage
from app.files.interfaces.services import FileService
from app.files.interfaces.uow import AbstractFileUoW

logger = get_logger()


IMAGES_MIMES = [
    "image/png",
    "image/webp",
    "image/jpeg",
    "image",
]


VIDEO_MIMES = [
    "video/mpeg",
    "video/mp4",
]


def get_type_by_mime_type(mime_type: str) -> FileEntityTypes | None:
    mime_type = mime_type.strip(" ")
    if mime_type in IMAGES_MIMES:
        return PhotoEntity
    elif mime_type in VIDEO_MIMES:
        return VideoEntity
    else:
        raise ValueError("not supported type", mime_type)


def get_dto_type_by_ent(file: FileDTOTypes) -> Type[FileDTOTypes]:
    if file is PhotoEntity or isinstance(file, PhotoEntity):
        return PhotoDTO
    elif file is DocumentEntity or isinstance(file, DocumentEntity):
        return DocumentDTO
    elif file is VideoEntity or isinstance(file, VideoEntity):
        return VideoDTO
    else:
        raise TypeError("not supported type")


class DownloadFromInternet:
    pass


class UploadStreamDownload:
    pass



class _SaveFile:
    def __init__(
        self,

    ):
        pass



class FileServiceImpl(FileService):
    def __init__(
        self,
        uow: AbstractFileUoW,
        file_storage: AbstractFileStorage,
        session: ClientSession,
    ) -> None:
        self.file_storage = file_storage
        self.uow = uow
        self.session = session

    async def download_file_by_url(self, download_url: str) -> FileEntityTypes:
        async with self.session.get(str(download_url)) as response:
            if response.status != 200:
                raise UnableToDownloadFile(download_url)
            mime_type = response.headers.get("Content-Type")

            ent_type = get_type_by_mime_type(mime_type)
            if ent_type is PhotoEntity:
                file = PhotoEntity(
                    width=1000,  # stub
                    height=1000,  # stub
                )
            elif ent_type is DocumentEntity:
                file = DocumentEntity(
                )
            elif ent_type is VideoEntity:
                raise NotImplementedError
            else:
                raise ValueError("Not supported mime type")

            async with self.uow.transaction():
                path_url = await self.file_storage.upload(
                    body=response.content,
                    key=str(file.file_id),
                    mime_type=mime_type,
                )
                file.file_url = path_url
                # idk why, but this code is too fast.
                # somehow need to remove this awful peace of code....
                file_metadata = await self.uow.file.add_file(file)
                return file_metadata.value

    async def download_file(self, file: bytes) -> FileEntityTypes:
        file_ent = PhotoEntity(
            width=1000,  # stub
            height=1000,  # stub
        )

        local_file = StreamReader()
        local_file.feed_data(file)
        async with self.uow.transaction():
            path_url = await self.file_storage.upload(
                local_file,
                key=str(file_ent.file_id),
                mime_type="images",
            )
            file_ent.file_url = path_url
            file_metadata = await self.uow.file.add_file(file)
            return file_metadata.value

    async def upload_file(
            self,
            file_dto: InputFile | str,
            type_: FileEntityTypes = None
    ) -> FileEntityTypes:  # не менять на дто сломается все
        if isinstance(file_dto, str):
            url = file_dto
        else:
            url = file_dto.download_url
        if url:
            file = await self.uow.file.file_by_url(url, FileEntity)
            if not file:
                file = await self.download_file_by_url(url)
        elif file_dto.file:
            file = await self.download_file(file_dto.file)
        elif file_dto.file_id:
            file = await self.uow.file.file_by_unique_id(file_dto.file_id, FileEntity)
        else:
            raise ValueError("No fileId, mimetype, or download url")
        if type_:
            if not isinstance(file, type_):
                raise FileTypeIncorrect

        return file
