from asyncio import StreamReader

from aiohttp import ClientSession

from app.base.logging.logger import get_logger
from app.base.use_cases import UseCase
from app.files.dtos.files import PhotoDTO, DocumentDTO, VideoDTO, FileDTOTypes
from app.files.dtos.input_file import InputFileType
from app.files.entities import FileEntityTypes, PhotoEntity, VideoEntity, DocumentEntity, FileEntity
from app.files.exceptions import UnableToDownloadFile
from app.files.file_storage.base import AbstractFileStorage, File
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

DOCUMENT_MIMES = [
    'application/pdf',
    'application/vnd.ms-powerpoint',
    'text/plain',
    'text/html',
]


def get_type_by_mime_type(mime_type: str) -> FileEntityTypes | None:
    mime_type = mime_type.strip(" ")
    if mime_type in IMAGES_MIMES:
        return PhotoEntity
    elif mime_type in VIDEO_MIMES:
        return VideoEntity
    elif mime_type in DOCUMENT_MIMES:
        return DocumentEntity
    else:
        raise ValueError("not supported type", mime_type)


dto_ent_to_types = {
    PhotoEntity: PhotoDTO,
    DocumentEntity: DocumentDTO,
    VideoEntity: VideoDTO,
}


def get_dto_type_by_ent(file: FileEntityTypes) -> FileDTOTypes:
    return dto_ent_to_types.get(file)


class DownloadFromInternet(UseCase[str, FileEntityTypes]):
    def __init__(
        self,
        file_storage: AbstractFileStorage,
        uow: AbstractFileUoW,
        aiohttp_session: ClientSession,
    ):
        self.aiohttp_session = aiohttp_session
        self.file_storage = file_storage
        self.uow = uow

    async def __call__(self, download_url: str) -> FileEntityTypes:
        async with self.aiohttp_session.get(download_url) as response:
            if response.status != 200:
                raise UnableToDownloadFile(download_url, str(response.status))
            mime_type = response.headers.get("Content-Type")

            downloader = DownloadFromBytes(self.file_storage, self.uow)
            return await downloader.download(response.content, mime_type=mime_type)


class DownloadFromBytes:
    def __init__(
            self,
            file_storage: AbstractFileStorage,
            uow: AbstractFileUoW,
    ):
        self.file_storage = file_storage
        self.uow = uow

    async def download(self, data: StreamReader | bytes, mime_type: str, key: str | None = None) -> FileEntityTypes:
        if isinstance(data, bytes):
            file_data = StreamReader()
            file_data.feed_data(data)
        async with self.uow.transaction():
            metadata = get_type_by_mime_type(mime_type)()

            file = File(
                body=data,
                key=str(key or metadata.file_id),
            )

            return await _SaveFile(
                file_storage=self.file_storage,
                uow=self.uow,
            )(file, metadata)


class _SaveFile:
    def __init__(
        self,
        file_storage: AbstractFileStorage,
        uow: AbstractFileUoW,
    ):
        self.file_storage = file_storage
        self.uow = uow

    async def __call__(self, file: File, metadata: FileEntityTypes) -> FileEntityTypes:
        async with self.uow.transaction():
            path_url = await self.file_storage.upload(file)
            metadata.file_url = path_url
            file_metadata = await self.uow.file.add_files(metadata)
            return file_metadata.value


class FilesServiceImpl(FileService):
    def __init__(
        self,
        file_storage: AbstractFileStorage,
        uow: AbstractFileUoW,
        aiohttp_session: ClientSession,
    ):
        self.file_storage = file_storage
        self.uow = uow
        self.aiohttp_session = aiohttp_session

    async def upload_file(self, file: InputFileType) -> FileEntityTypes:
        file_url = file if isinstance(file, str) else file.download_url
        if file_url:
            return await DownloadFromInternet(
                file_storage=self.file_storage,
                uow=self.uow,
                aiohttp_session=self.aiohttp_session,
            )(str(file_url))

        elif file.file:
            return await DownloadFromBytes(
                file_storage=self.file_storage,
                uow=self.uow,
            ).download(file.file, file.mime_type)
        elif file.file_id:
            return await self.uow.file.file_by_unique_id(
                file.file_id,
                FileEntity,
            )

        raise ValueError("Not correct Input file")
