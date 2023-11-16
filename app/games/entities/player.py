from ipaddress import IPv4Address, IPv6Address

from attr import field

from app.base.aggregate import Aggregate
from app.base.entity import TimedEntity
from app.games.value_objects.hours import Hours
from app.games.value_objects.ids import PlayerID
from app.games.value_objects.steam_id import SteamID


class PlayerEntity(TimedEntity, Aggregate):
	id: PlayerID = field(factory=PlayerID.generate)
	name: str
	steam_id: SteamID | None
	ipv4: IPv4Address | None
	ipv6: IPv6Address | None
	hours: Hours = field(default=Hours(0))
