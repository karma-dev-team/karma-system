from typing import Union, Type

from app.base.dto import DTO
from app.files.value_objects import FileID


class FileBase(DTO):
    file_id: FileID
    # need to make it to support relative urls
    file_url: str
    file_name: str | None
    mime_type: str | None
    file_size: int | None


class DocumentDTO(FileBase):
    file_unique_id: FileID


class PhotoDTO(FileBase):
    width: int
    height: int


class VideoDTO(FileBase):
    width: int
    height: int
    duration: int  # in seconds


# dont wrap Union into Type, it will crash fastapi
FileDTOTypes = Union[DocumentDTO, PhotoDTO, VideoDTO]
