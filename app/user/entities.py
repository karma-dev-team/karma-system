from app.base.entity import TimedEntity, entity
from app.user.enums import UserRoles
from app.user.value_objects import UserID


@entity
class UserEntity(TimedEntity):
	id: UserID
	role: UserRoles
	name: str
	email: str

	# @classmethod
	# def create(cls, ):
