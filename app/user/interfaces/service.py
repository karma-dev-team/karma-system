from abc import abstractmethod

from app.user.dto.user import GetUserDTO, UserDTO, CreateUserDTO, RegCodeDTO, CreateRegCode, UpdateUserDTO


class AbstractUserService:
	@abstractmethod
	async def get_user(self, dto: GetUserDTO) -> UserDTO:
		pass

	@abstractmethod
	async def create_user(self, dto: CreateUserDTO) -> UserDTO:
		pass

	@abstractmethod
	async def create_reg_code(self) -> RegCodeDTO:
		pass

	@abstractmethod
	async def update_user(self, dto: UpdateUserDTO) -> UserDTO:
		pass
