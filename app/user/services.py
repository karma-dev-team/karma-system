from app.user.interfaces import AbstractUserService
from app.user.value_objects import UserID


class UserService(AbstractUserService):
	async def get_user(self, user_id: UserID):
		pass

	async def create_user(self, dto: CreateUserDTO) -> UserDTO:
		pass
