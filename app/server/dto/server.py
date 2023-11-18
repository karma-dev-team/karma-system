from ipaddress import IPv4Address
from typing import Sequence

from app.base.dto import DTO, TimedDTO
from app.games.value_objects.ids import GameID
from app.server.dto.player import GetPlayerDTO
from app.server.value_objects.amount import ServerKarmaAmount
from app.server.value_objects.ids import ServerID
from app.user.dto.user import UserDTO
from app.user.value_objects import UserID


class GetServerDTO(DTO):
	server_id: ServerID
	name: str


class ServerDTO(DTO, TimedDTO):
	name: str
	port: int
	ip: IPv4Address
	owner_id: UserID
	owner: UserDTO
	karma: ServerKarmaAmount
	game_id: GameID


class GetPlayersKarmaDTO(DTO):
	players: Sequence[GetPlayerDTO]


class RegisterServerDTO(DTO):
	name: str
	port: int
	ip: IPv4Address
