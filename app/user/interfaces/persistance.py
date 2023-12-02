import abc
from typing import Protocol

from app.base.database.result import Result
from app.user.entities import UserEntity
from app.user.exceptions import EmailAlreadyTaken, UserAlreadyExists
from app.user.value_objects import UserID


class AbstractUserRepo(Protocol):
	@abc.abstractmethod
	async def get_user_by_id(self, user_id: UserID) -> UserEntity:
		pass

	@abc.abstractmethod
	async def add_user(
			self, user: UserEntity, reg_code: str
	) -> Result[UserEntity, EmailAlreadyTaken | UserAlreadyExists | RegistrationCodeIsNotCorrect]:
		pass
