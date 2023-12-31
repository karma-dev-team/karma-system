from datetime import datetime
from ipaddress import IPv4Address, IPv6Address

from pydantic import Field

from app.base.dto import DTO, TimedDTO
from app.server.value_objects.hours import Hours
from app.server.value_objects.ids import PlayerID
from app.server.value_objects.steam_id import SteamID


class GetPlayerDTO(DTO):
	steam_id: SteamID | None
	ipv4: IPv4Address | None
	ipv6: IPv6Address | None
	name: str | None


class PlayerDTO(DTO):
	id: PlayerID
	created_at: datetime = Field(default_factory=datetime.now)
	name: str
	steam_id: SteamID | None
	ipv4: IPv4Address | None
	ipv6: IPv6Address | None
	hours: Hours = Hours(0)
