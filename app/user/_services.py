from app.base.value_objects.ids import UIDValueObject
from app.user.interfaces import AbstractUserService


class UserServiceImpl(AbstractUserService):
	async def get_user(self, user_id: UIDValueObject):
		pass
