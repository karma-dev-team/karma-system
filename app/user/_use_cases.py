from app.base.use_cases import UseCase
from app.user.dto.user import GetUserDTO, UserDTO


class GetUser(UseCase[GetUserDTO, UserDTO]):
	async def __call__(self, dto: GetUserDTO) -> UserDTO:
		pass
