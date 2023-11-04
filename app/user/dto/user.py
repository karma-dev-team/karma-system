from app.infrastructure.dto import DTO
from app.user.value_objects import UserID


class GetUserDTO(DTO):
	user_id: UserID


class UserDTO(DTO):
	id: UserID
