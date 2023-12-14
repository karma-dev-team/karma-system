import uuid
from hashlib import md5

import bcrypt
from attrs import field
from attrs.validators import instance_of, max_len, optional

from app.base.aggregate import Aggregate
from app.base.entity import TimedEntity, entity
from app.user.dto.user import UserDTO
from app.user.enums import UserRoles
from app.user.events.user import UserCreated, GivenSuperUser, UserBlocked
from app.user.exceptions import RegistrationCodeAlreadyUsed
from app.user.security import get_password_hash, verify_password
from app.user.value_objects import UserID, RegCodeID


@entity
class UserEntity(TimedEntity, Aggregate):
	id: UserID = field(factory=UserID.generate)
	role: UserRoles = field(validator=instance_of(UserRoles), default=UserRoles.user)
	name: str
	email: str
	hashed_password: str = field(validator=instance_of(str))
	blocked: bool = field(default=False)
	superuser: bool = field(default=False)

	@classmethod
	def create(
		cls,
		name: str,
		email: str,
		hashed_password: str,
		role: UserRoles = UserRoles.user,
	) -> "UserEntity":
		user = UserEntity(
			name=name,
			email=email,
			hashed_password=hashed_password,
			role=role,
		)

		user.add_event(
			UserCreated(
				user=UserDTO.model_validate(user)
			)
		)

		return user

	def give_superuser(self, by: "UserEntity") -> None:
		self.superuser = True
		self.add_event(
			GivenSuperUser(
				by=UserDTO.model_validate(by),
				user=UserDTO.model_validate(self)
			)
		)

	@staticmethod
	def create_password(password: str) -> str:
		# имеются сайд эффекты
		return get_password_hash(password)

	@staticmethod
	def verify_password(password: str, hashed_password: str) -> bool:
		return verify_password(password, hashed_password)

	def block(self):
		if self.blocked:
			raise ValueError("User already blocked")
		self.blocked = True

		self.add_event(
			UserBlocked(
				UserDTO.model_validate(self)
			)
		)


@entity
class RegistrationCodeEntity(TimedEntity):
	# if user_id is not None then reg code is used!
	id: RegCodeID = field(factory=RegCodeID.generate)
	key: str = field(validator=max_len(64))
	code: str = field(validator=max_len(64))
	user_id: UserID = field(validator=optional(instance_of(UserID)), default=None)

	@staticmethod
	def generate_reg_code(key: str | None = None) -> str:
		return md5(str(key or uuid.uuid4()).encode("utf8")).hexdigest()

	@classmethod
	def create(cls, key: str) -> "RegistrationCode":
		reg = RegistrationCodeEntity(
			key=key,
			code=cls.generate_reg_code(key),
		)

		return reg

	def register_user(self, user_id: UserID):
		if self.user_id:
			raise RegistrationCodeAlreadyUsed(self.id)
		self.user_id = user_id
