from typing import Union, Type

from app.application.common.dto import DTO
from app.domain.common.value_objects.uuid import DomainID


class FileBase(DTO):
    file_id: DomainID
    # need to make it to support relative urls
    file_url: str
    file_name: str | None
    mime_type: str | None
    file_size: int | None


class DocumentDTO(FileBase):
    file_unique_id: DomainID


class PhotoDTO(FileBase):
    width: int
    height: int


class VideoDTO(FileBase):
    width: int
    height: int
    duration: int  # in seconds


# dont wrap Union into Type, it will crash fastapi
FileDTOTypes = Union[DocumentDTO, PhotoDTO, VideoDTO]
