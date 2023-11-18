from ipaddress import IPv4Address, IPv6Address

from attr import field, asdict

from app.base.aggregate import Aggregate
from app.base.entity import TimedEntity, entity
from app.games.dto.player import PlayerDTO
from app.server.value_objects.hours import Hours
from app.server.value_objects.ids import PlayerID
from app.server.value_objects.steam_id import SteamID


@entity
class PlayerSelector:
	steam_id: SteamID | None
	ipv4: IPv4Address | None
	ipv6: IPv6Address | None

	@classmethod
	def create(cls, **kwargs):
		if not any(kwargs.values()):
			raise ValueError("Steam id, ipv4, ipv6 are not provided.")
		ent = PlayerEntity(**kwargs)

		return ent


@entity
class PlayerEntity(TimedEntity, Aggregate):
	id: PlayerID = field(factory=PlayerID.generate)
	name: str
	steam_id: SteamID | None
	ipv4: IPv4Address | None
	ipv6: IPv6Address | None
	hours: Hours = field(default=Hours(0))

	@classmethod
	def create(cls, name: str, selector: PlayerSelector) -> "PlayerEntity":
		data = asdict(selector)

		ent = PlayerEntity(
			name=name,
			**data,
		)

		ent.add_event(
			PlayerCreated(
				player=PlayerDTO(
					name=name,
					**data,
				)
			)
		)

		return ent

