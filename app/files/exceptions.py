from app.base.exceptions import ApplicationError


class FileNotExists(ApplicationError):
	def message(self) -> str:
		return "File not exists"


class FileTypeIncorrect(ApplicationError):
	def message(self) -> str:
		return "File type incorrect"


class UnableToDownloadFile(ApplicationError):
	download_url: str

	def message(self) -> str:
		return "unable to download file"
