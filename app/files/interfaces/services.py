import abc

from app.files.dtos.input_file import InputFileType
from app.files.entities import FileEntityTypes


class FileService:
	@abc.abstractmethod
	async def upload_file(self, file: InputFileType) -> FileEntityTypes:
		pass