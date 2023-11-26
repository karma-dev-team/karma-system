from attrs import define

exception_wrapper = define()


class APIError(Exception):
	def message(self) -> str:
		return "General API Error"


class ApplicationError(Exception):
	def message(self) -> str:
		return "Application Error"


class DomainError(Exception):
	pass


class RepositoryError(ApplicationError):
	pass
