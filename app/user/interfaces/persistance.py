import abc
from dataclasses import Field, field
from typing import Protocol, Tuple

from app.base.database.filters import filter_wrapper
from app.base.database.result import Result
from app.user.entities import UserEntity, RegistrationCodeEntity
from app.user.exceptions import EmailAlreadyTaken, UserAlreadyExists, RegistrationCodeIsNotCorrect
from app.user.value_objects import UserID


@filter_wrapper
class GetUserFilter:
	name: str | None = field(default=None)
	email: str | None = field(default=None)
	user_id: UserID | None = field(default=None)


class AbstractUserRepo(Protocol):
	@abc.abstractmethod
	async def get_user_by_id(self, user_id: UserID) -> UserEntity | None:
		pass

	@abc.abstractmethod
	async def get_user_by_filters(self, filter: GetUserFilter) -> UserEntity | None:
		pass

	@abc.abstractmethod
	async def add_user(
			self, user: UserEntity, reg_code: str
	) -> Result[Tuple[UserEntity, RegistrationCodeEntity], EmailAlreadyTaken | UserAlreadyExists | RegistrationCodeIsNotCorrect]:
		pass

	@abc.abstractmethod
	async def add_reg_code(
			self, reg_code: RegistrationCodeEntity
	) -> Result[RegistrationCodeEntity, None]:
		"""Registration code has only one method, that's why it belongs to UserRepo"""
		pass
