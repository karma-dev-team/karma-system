
from attrs import field
from attrs.validators import instance_of, optional
from pydantic_core import Url

from app.base.entity import entity
from app.files.value_objects import FileID


@entity
class FileEntity:
    file_id: FileID = field(factory=FileID.generate)
    file_url: Url | str | None = field(
        validator=optional(instance_of((Url, str))),
        default=None,
    )
    file_name: str | None = field(validator=optional(instance_of(str)), default=None)
    mime_type: str | None = field(validator=optional(instance_of(str)), default=None)
    file_size: int | None = field(validator=optional(instance_of(int)), default=0)


@entity
class PhotoEntity(FileEntity):
    width: int = field(validator=instance_of(int))
    height: int = field(validator=instance_of(int))

    @classmethod
    def create_photo(
        cls,
        width: int,
        height: int,
        file_url: str | Url,
        mime_type: str | None = None,
        file_name: str | None = None,
    ) -> "PhotoEntity":
        return PhotoEntity(
            width=width,
            height=height,
            file_url=file_url,
            file_name=file_name,
            mime_type=mime_type,
        )


@entity
class VideoEntity(FileEntity):
    width: int = field(validator=instance_of(int))
    height: int = field(validator=instance_of(int))
    duration: int = field(validator=instance_of(int))

    @classmethod
    def create_video(
        cls,
        width: int,
        height: int,
        file_url: str | Url,
        duration: int,
        mime_type: str | None = None,
        file_name: str | None = None,
    ) -> "VideoEntity":
        return VideoEntity(
            width=width,
            duration=duration,
            height=height,
            file_url=file_url,
            file_name=file_name,
            mime_type=mime_type,
        )


@entity
class DocumentEntity(FileEntity):
    @classmethod
    def create_document(
            cls,
            file_url: str | Url,
            mime_type: str | None = None,
            file_name: str | None = None,
    ) -> "DocumentEntity":
        return DocumentEntity(
            file_url=file_url,
            file_name=file_name,
            mime_type=mime_type,
        )


FileEntityTypes = DocumentEntity | VideoEntity | PhotoEntity
