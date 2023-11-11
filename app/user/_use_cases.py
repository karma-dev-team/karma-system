from app.base.use_cases import UseCase
from app.user.dto.user import GetUserDTO, UserDTO
from app.user.value_objects import UserID


class GetUser(UseCase[GetUserDTO, UserDTO]):
	async def __call__(self, dto: GetUserDTO) -> UserDTO:
		return UserDTO(id=UserID.generate())
