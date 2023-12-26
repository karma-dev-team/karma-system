from __future__ import annotations

import os
from typing import TYPE_CHECKING

from app.auth.access_policy import BasicAccessPolicy
from app.auth.exceptions import AccessDenied
from app.base.database.result import Result
from app.base.events.dispatcher import EventDispatcher
from app.files.interfaces.services import FileService
from app.user.dto.user import CreateUserDTO, UserDTO, GetUserDTO, CreateRegCode, RegCodeDTO, UpdateUserDTO
from app.user.entities import UserEntity, RegistrationCodeEntity
from app.user.enums import USER_ROLES_AS_INTEGER, UserRoles
from app.user.exceptions import UserAlreadyExists, UserDoesNotExists, EmailAlreadyTaken, UsernameAlreadyTaken
from app.user.interfaces import AbstractUserService
from app.user.interfaces.persistance import GetUserFilter
from app.user.interfaces.uow import AbstractUserUoW

if TYPE_CHECKING:
	from app.base.config import GlobalConfig


class UserService(AbstractUserService):
	def __init__(
			self,
			uow: AbstractUserUoW,
			event_dispatcher: EventDispatcher,
			access_policy: BasicAccessPolicy,
			config: GlobalConfig,
			file_service: FileService,
	) -> None:
		self.file_service = file_service
		self.uow = uow
		self.event_dispatcher = event_dispatcher
		self.access_policy = access_policy
		self.config = config

	async def get_user(self, dto: GetUserDTO) -> UserDTO:
		user = await self.uow.user.get_user_by_filters(
			GetUserFilter(
				user_id=dto.user_id,
				name=dto.name,
				email=dto.email,
			)
		)
		if not user:
			raise UserDoesNotExists(dto.name or dto.email or dto.user_id)
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
				case Result(value, None):
					result_user, code = value
					code.register_user(result_user.id)

					await self.event_dispatcher.publish_events(user.events)

					return UserDTO.model_validate(result_user)
				case Result(_, UsernameAlreadyTaken() as err):
					user = await self.uow.user.get_user_by_filters(
						GetUserFilter(
							name=user.name,
						)
					)
					return UserDTO.model_validate(user)
				case Result(_, EmailAlreadyTaken() as err):
					user = await self.uow.user.get_user_by_filters(
						GetUserFilter(
							email=user.email,
						)
					)
					return UserDTO.model_validate(user)
				case Result(_, err):
					raise err

	async def create_reg_code(self) -> RegCodeDTO:
		if not self.config.debug:
			if self.access_policy.as_int() >= self.access_policy.role_as_int(UserRoles.moderator):
				raise AccessDenied

		key = os.urandom(32).hex()
		reg_code = RegistrationCodeEntity.create(key)

		async with self.uow.transaction():
			result = await self.uow.user.add_reg_code(reg_code)

			return RegCodeDTO.model_validate(result.value)

	async def update_user(self, dto: UpdateUserDTO) -> UserDTO:
		if (
			self.access_policy.anonymous()
			or self.access_policy.user.id != dto.user_id
			or not self.access_policy.check_role(UserRoles.admin)
		):
			raise AccessDenied

		user = await self.uow.user.get_user_by_id(dto.user_id)

		if dto.data.email:
			user.email = dto.data.email
		if dto.data.role:
			if self.access_policy.check_role(UserRoles.admin):
				user.role = dto.data.role
			else:
				raise AccessDenied
		if dto.data.name:
			user.name = dto.data.name
		if dto.data.image:
			photo = await self.file_service.upload_file(dto.data.image)
			user.photo = photo

		async with self.uow.transaction():
			result = await self.uow.user.update_user(user)
			match result:
				case Result(value, None):
					return UserDTO.model_validate(value)
				case Result(None, EmailAlreadyTaken() as exc):
					raise exc
