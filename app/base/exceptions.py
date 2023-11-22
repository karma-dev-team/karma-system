class APIError(Exception):
	pass


class ApplicationError(Exception):
	pass


class DomainError(Exception):
	pass


class RepositoryError(ApplicationError):
	pass
