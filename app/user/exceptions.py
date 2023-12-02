from app.base.exceptions import RepositoryError, ApplicationError


class EmailAlreadyTaken(RepositoryError):
	pass


class UserAlreadyExists(ApplicationError):
	def message(self) -> str:
		return "user already exists in rdbms"


class RegistrationCodeIsNotCorrect(ApplicationError):
	def message(self) -> str:
		return "registration code is not found"
