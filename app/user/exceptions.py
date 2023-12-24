from app.base.exceptions import RepositoryError, ApplicationError
from app.user.value_objects import UserID, RegCodeID


class EmailAlreadyTaken(RepositoryError):
	pass


class UserAlreadyExists(ApplicationError):
	def message(self) -> str:
		return "user already exists in rdbms"


class RegistrationCodeIsNotCorrect(ApplicationError):
	def message(self) -> str:
		return "registration code is not found"


class UserDoesNotExists(ApplicationError):
	user_id: UserID | None

	def message(self) -> str:
		return f"user does not exists, id: {self.user_id}"


class RegistrationCodeAlreadyUsed(ApplicationError):
	reg_code_id: RegCodeID

	def message(self) -> str:
		return "registration code id already used"
