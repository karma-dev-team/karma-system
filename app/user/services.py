from app.user.dto.user import CreateUserDTO, UserDTO, GetUserDTO
from app.user.entities import UserEntity
from app.user.interfaces import AbstractUserService
from app.user.interfaces.uow import AbstractUserUoW


class UserService(AbstractUserService):
	def __init__(self, uow: AbstractUserUoW) -> None:
		self.uow = uow

	async def get_user(self, dto: GetUserDTO):
		pass

	async def create_user(self, dto: CreateUserDTO) -> UserDTO:
		user = UserEntity.create(
			name=dto.name,
			email=dto.email,
			hashed_password=dto.hashed_password,
		)
		result = await self.uow.user.add_user(user, dto.registration_code)
