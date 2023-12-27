from ipaddress import IPv4Address, IPv6Address
from typing import Sequence

from pydantic import Field
from pydantic_core import Url

from app.base.dto import DTO, TimedDTO
from app.files.dtos.files import PhotoDTO
from app.files.dtos.input_file import InputFileType
from app.games.dto.game import GameDTO
from app.games.value_objects.ids import GameID
from app.server.dto.player import GetPlayerDTO
from app.karma.value_objects.karma import KarmaAmount
from app.server.value_objects.ids import ServerID
from app.user.dto.user import UserDTO
from app.user.value_objects import UserID


class GetServerDTO(DTO):
	server_id: ServerID | None = Field(default=None)
	name: str | None = Field(default=None)


class ServerDTO(DTO, TimedDTO):
	id: ServerID
	name: str
	port: int
	ipv4: str
	ipv6: str | None = Field(default=None)
	owner_id: UserID
	owner: UserDTO | None
	karma: KarmaAmount
	game_id: GameID
	game: GameDTO
	icon: PhotoDTO | None = Field(default=None)

	def full_ip(self) -> str:
		ip = self.ipv4
		# bug when checking for ipv6
		# python and pydantic counts it as real value
		# and ignores that ipv6 is None!!
		# and continues with ipv6 empty one
		# if str(self.ipv6) is not None:
		# 	ip = self.ipv6
		return ip + ":" + str(self.port)


class GetPlayersKarmaDTO(DTO):
	players: Sequence[GetPlayerDTO]


class ApproveServersDTO(DTO):
	server_ids: Sequence[ServerID]


class QueueServerDTO(DTO):
	name: str
	description: str
	icon: InputFileType | None = Field(default=None)
	country_code: str = "RU"
	port: int
	game_id: GameID
	ip: IPv4Address
	tags: list[str] = []
	website_link: Url | None = Field(default=None)
	discord_link: Url | None = Field(default=None)


class GetServersDTO(DTO):
	tags: list[str] | None = Field(default=None)
	game: str | None = Field(default=None)
	unregistered: bool | None = Field(default=None)
	name: str | None = Field(default=None)
	category: str | None = Field(default=None)
