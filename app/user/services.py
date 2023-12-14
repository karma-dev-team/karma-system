from app.auth.access_policy import BasicAccessPolicy
from app.auth.exceptions import AccessDenied
from app.base.database.result import Result
from app.base.events.dispatcher import EventDispatcher
from app.user.dto.user import CreateUserDTO, UserDTO, GetUserDTO, CreateRegCode, RegCodeDTO
from app.user.entities import UserEntity, RegistrationCodeEntity
from app.user.enums import USER_ROLES_AS_INTEGER, UserRoles
from app.user.exceptions import UserAlreadyExists
from app.user.interfaces import AbstractUserService
from app.user.interfaces.persistance import GetUserFilter
from app.user.interfaces.uow import AbstractUserUoW


class UserService(AbstractUserService):
	def __init__(
			self,
			uow: AbstractUserUoW,
			event_dispatcher: EventDispatcher,
			access_policy: BasicAccessPolicy
	) -> None:
		self.uow = uow
		self.event_dispatcher = event_dispatcher
		self.access_policy = access_policy

	async def get_user(self, dto: GetUserDTO) -> UserDTO:
		user = await self.uow.user.get_user_by_filters(
			GetUserFilter(
				user_id=dto.user_id,
				name=dto.name,
				email=dto.email,
			)
		)
		return UserDTO.model_validate(user)

	async def create_user(self, dto: CreateUserDTO) -> UserDTO:
		user = await self.uow.user.get_user_by_filters(
			GetUserFilter(
				name=dto.name,
				email=dto.email,
			)
		)
		if user:
			raise UserAlreadyExists()
		user = UserEntity.create(
			name=dto.name,
			email=dto.email,
			hashed_password=UserEntity.create_password(dto.password),
		)
		async with self.uow.transaction():
			result = await self.uow.user.add_user(user, dto.registration_code)

			match result:
				case Result(value, _):
					result_user, code = value
					code.register_user(result_user)

					await self.event_dispatcher.publish_events(user.events)

					return UserDTO.model_validate(result_user)
				case Result(_, UserAlreadyExists() as err):
					user = await self.uow.user.get_user_by_id(user.id)
					return UserDTO.model_validate(user)
				case Result(_, err):
					raise err

	async def create_reg_code(self, dto: CreateRegCode) -> RegCodeDTO:
		if self.access_policy.as_int() >= self.access_policy.role_as_int(UserRoles.moderator):
			raise AccessDenied
		reg_code = RegistrationCodeEntity.create(dto.key)

		async with self.uow.transaction():
			result = await self.uow.user.add_reg_code(reg_code)

			return RegCodeDTO.model_validate(result.value)
