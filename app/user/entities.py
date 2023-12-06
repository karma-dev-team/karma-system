from attrs import field
from attrs.validators import instance_of

from app.base.aggregate import Aggregate
from app.base.entity import TimedEntity, entity
from app.server.security import generate_jwt
from app.user.dto.user import UserDTO
from app.user.enums import UserRoles
from app.user.events.user import UserCreated, GivenSuperUser, UserBlocked
from app.user.security import get_password_hash, verify_password
from app.user.value_objects import UserID


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
