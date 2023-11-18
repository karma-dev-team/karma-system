from ipaddress import IPv6Address, IPv4Address

from app.base.dto import DTO, TimedDTO
from app.server.value_objects.hours import Hours
from app.server.value_objects.ids import PlayerID
from app.server.value_objects.steam_id import SteamID


class PlayerDTO(DTO, TimedDTO):
	id: PlayerID
	name: str
	steam_id: SteamID | None
	ipv4: IPv4Address | None
	ipv6: IPv6Address | None
	hours: Hours = Hours(0)
