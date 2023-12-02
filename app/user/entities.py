from attrs import field
from attrs.validators import instance_of

from app.base.aggregate import Aggregate
from app.base.entity import TimedEntity, entity
from app.user.dto.user import UserDTO
from app.user.enums import UserRoles
from app.user.events.user import UserCreated, GivenSuperUser
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

		user.add_event(UserCreated(UserDTO.model_validate(user)))

		return user

	def give_superuser(self, by: "UserEntity") -> None:
		self.superuser = True
		self.add_event(
			GivenSuperUser(
				by=UserDTO.model_validate(by),
				user=UserDTO.model_validate(self)
			)
		)
