from ipaddress import IPv4Address
from typing import Sequence

from app.base.dto import DTO
from app.games.value_objects.ids import GameID
from app.server.value_objects.amount import ServerKarmaAmount
from app.server.value_objects.ids import ServerID
from app.user.dto.user import UserDTO
from app.user.value_objects import UserID


class GetServerIdDTO(DTO):
	server_id: ServerID
	name: str


class ServerDTO(DTO):
	name: str
	port: int
	ip: IPv4Address
	owner_id: UserID
	owner: UserDTO
	karma: ServerKarmaAmount
	game_id: GameID


class GetPlayersKarmaDTO:
	players: Sequence[GetPlayerDTO]

