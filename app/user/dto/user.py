from app.base.dto import DTO
from app.user.enums import UserRoles
from app.user.value_objects import UserID


class GetUserDTO(DTO):
	user_id: UserID | None
	email: str | None
	name: str | None


class UserDTO(DTO):
	id: UserID
	name: str
	email: str
	hashed_password: str
	role: UserRoles = UserRoles.user
	blocked: bool = False


class CreateUserDTO(DTO):
	name: str
	email: str
	hashed_password: str
	registration_code: str
