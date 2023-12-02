from app.base.database.result import Result
from app.base.events.dispatcher import EventDispatcher
from app.user.dto.user import CreateUserDTO, UserDTO, GetUserDTO
from app.user.entities import UserEntity
from app.user.exceptions import UserAlreadyExists
from app.user.interfaces import AbstractUserService
from app.user.interfaces.persistance import GetUserFilter
from app.user.interfaces.uow import AbstractUserUoW


class UserService(AbstractUserService):
	def __init__(self, uow: AbstractUserUoW, event_dispatcher: EventDispatcher) -> None:
		self.uow = uow
		self.event_dispatcher = event_dispatcher

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
		user = UserEntity.create(
			name=dto.name,
			email=dto.email,
			hashed_password=dto.hashed_password,
		)
		async with self.uow.transaction():
			result = await self.uow.user.add_user(user, dto.registration_code)

			match result:
				case Result(value, _):
					await self.event_dispatcher.publish_events(user.events)

					return UserDTO.model_validate(value)
				case Result(_, UserAlreadyExists() as err):
					user = await self.uow.user.get_user_by_id(user.id)
					return UserDTO.model_validate(user)
				case Result(_, err):
					raise err
