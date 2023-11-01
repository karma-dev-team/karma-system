from abc import abstractmethod

from app.base.value_objects.ids import UIDValueObject


class AbstractUserService:
	@abstractmethod
	async def get_user(self, user_id: UIDValueObject):
		pass
