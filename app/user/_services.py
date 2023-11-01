from app.user.interfaces import AbstractUserService
from app.user.value_objects import UserID


class UserServiceImpl(AbstractUserService):
	async def get_user(self, user_id: UserID):
		pass
