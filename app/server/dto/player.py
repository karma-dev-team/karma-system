from ipaddress import IPv4Address, IPv6Address

from app.base.dto import DTO
from app.server.value_objects.steam_id import SteamID


class GetPlayerDTO(DTO):
	steam_id: SteamID | None
	ipv4: IPv4Address | None
	ipv6: IPv6Address | None
	name: str | None
