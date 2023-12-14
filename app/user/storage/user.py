from typing import Tuple

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.base.database.repo import SQLAlchemyRepo
from app.base.database.result import Result
from app.user.entities import UserEntity, RegistrationCodeEntity
from app.user.exceptions import EmailAlreadyTaken, UserAlreadyExists, RegistrationCodeIsNotCorrect
from app.user.interfaces import AbstractUserRepo
from app.user.interfaces.persistance import GetUserFilter
from app.user.value_objects import UserID


class UserRepoImpl(AbstractUserRepo, SQLAlchemyRepo):
	def _parse_error(self, err: IntegrityError, user: UserEntity):
		if not hasattr(err.__cause__.__cause__, "constraint_name"):
			raise err
		match err.__cause__.__cause__.constraint_name:  # type: ignore
			case "pk_users":
				return UserAlreadyExists(user.id)
			case "ix_users_username":
				return UserAlreadyExists(str(user.name))
			case 'ix_users_email':
				return UserAlreadyExists(str(user.email))
			case _:
				raise err

	async def get_user_by_id(self, user_id: UserID) -> UserEntity | None:
		user = await self.session.get(
			entity=UserEntity,
			ident=str(user_id),
			populate_existing=True,
		)
		return user

	async def get_user_by_filters(self, filter: GetUserFilter) -> UserEntity | None:
		stmt = select(UserEntity)

		if filter.email is not None:
			stmt = stmt.where(UserEntity.email == filter.email)
		if filter.name is not None:
			stmt = stmt.where(UserEntity.name == filter.name)
		if filter.user_id is not None:
			stmt = stmt.where(UserEntity.id == str(filter.id))

		result = await self.session.execute(stmt)
		return result.unique().scalar_one_or_none()

	async def add_user(
			self, user: UserEntity, reg_code: str
	) -> Result[
		Tuple[UserEntity, RegistrationCodeEntity],
		EmailAlreadyTaken | UserAlreadyExists | RegistrationCodeIsNotCorrect
	]:
		code = await self._get_reg_code(reg_code)
		if not code:
			raise RegistrationCodeIsNotCorrect()
		self.session.add(user)

		try:
			await self.session.flush((user,))
		except IntegrityError as err:
			return Result.fail(self._parse_error(err, user))

		return Result.ok((user, code))

	async def _get_reg_code(self, code: str) -> RegistrationCodeEntity | None:
		stmt = (select(RegistrationCodeEntity).where(
			RegistrationCodeEntity.code == code))

		result = await self.session.execute(stmt)
		return result.unique().scalar_one_or_none()

	async def add_reg_code(
			self, reg_code: RegistrationCodeEntity
	) -> Result[RegistrationCodeEntity, None]:
		self.session.add(reg_code)

		try:
			await self.session.flush((reg_code,))
		except IntegrityError as err:
			# fck u
			return Result.fail(err)

		return Result.ok(reg_code)
