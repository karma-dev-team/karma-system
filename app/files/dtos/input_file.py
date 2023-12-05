from pydantic_core import Url

from app.base.dto import DTO
from app.base.typeid import TypeID


class InputFile(DTO):
    """
    Как бы не является dto, но от части является.
    Отвечает за информацию для загрузки файла.
    Если был передан file_id то репозитории пытается найти
    по file_id.
    """
    file_id: TypeID | None
    mime_type: str | None
    download_url: Url | None


InputFileType = InputFile | str
