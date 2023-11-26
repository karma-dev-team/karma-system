from attr import field
from attr.converters import optional
from attr.validators import instance_of

from app.base.exceptions import APIError, ApplicationError, exception_wrapper
from app.server.dto.player import GetPlayerDTO
from app.server.value_objects.ids import PlayerID, ServerID


@exception_wrapper
class IncorrectAPIServerToken(APIError):
	token: str

	def message(self) -> str:
		return 'Incorrect server api token'


@exception_wrapper
class PlayerDoesNotExists(ApplicationError):
	player_id: PlayerID | None = field(validator=optional(instance_of(PlayerID)))
	ply_data: GetPlayerDTO | None = field(validator=optional(instance_of(GetPlayerDTO)))

	def message(self) -> str:
		return f"Specified player does not exists, ID: {self.player_id}"


class ServerNotExists(ApplicationError):
	server_id: ServerID

	def message(self) -> str:
		return f"Specified server does not exists, ID: {self.server_id}"
