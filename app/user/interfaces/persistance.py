import abc

from app.user.entities import UserEntity
from app.user.value_objects import UserID


class AbstractUserRepo:
	@abc.abstractmethod
	async def get_user_by_id(self, user_id: UserID) -> UserEntity:
		pass
