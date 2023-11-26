from abc import abstractmethod

from app.user.dto.user import GetUserDTO, UserDTO


class AbstractUserService:
	@abstractmethod
	async def get_user(self, dto: GetUserDTO) -> UserDTO:
		pass
