from typing import Any, Dict

from pydantic import root_validator

from app.application.common.dto import DTO
from app.domain.common.value_objects.url import URLValueObject
from app.domain.common.value_objects.uuid import DomainID


class InputFile(DTO):
    """
    Как бы не является dto, но от части является.
    Отвечает за информацию для загрузки файла.
    Если был передан file_id то репозитории пытается найти
    по file_id.
    """
    file_id: DomainID | None
    mime_type: str | None
    download_url: URLValueObject | None


InputFileType = InputFile | str
