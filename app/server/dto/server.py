from app.base.dto import DTO
from app.base.value_objects.ids import IPUIDValueObject
from app.server.value_objects import ServerID, ServerKarmaAmount
from app.user.dto.user import UserDTO
from app.user.value_objects import UserID


class GetServerIdDTO(DTO):
	server_id: ServerID
	name: str


class ServerDTO(DTO):
	name: str
	port: int
	ip: IPUIDValueObject
	owner_id: UserID
	owner: UserDTO
	karma: ServerKarmaAmount
