from ipaddress import IPv4Address, IPv6Address

from attrs import field, asdict
from attrs.validators import optional, instance_of

from app.base.aggregate import Aggregate
from app.base.entity import TimedEntity, entity
from app.server.dto.player import PlayerDTO
from app.karma.value_objects.karma import KarmaAmount
from app.server.events.player import PlayerCreated, PlayerKarmaChanged, PlayerConnected
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
	steam_id: SteamID | None = field(validator=optional(instance_of(SteamID)), default=None)
	ipv4: IPv4Address | None = field(validator=optional(instance_of(IPv4Address)), default=None)
	ipv6: IPv6Address | None = field(validator=optional(instance_of(IPv6Address)), default=None)
	hours: Hours = field(default=Hours(0))
	karma: KarmaAmount = field(default=KarmaAmount(0))
	online: bool = field(default=False)

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

	def change_karma(self, delta_karma: KarmaAmount) -> None:
		self.karma -= delta_karma

		self.add_event(
			PlayerKarmaChanged(
				ply=PlayerDTO.model_validate(self)
			)
		)

	def player_connectod(self):
		self.online = True
		self.add_event(
			PlayerConnected(
				player=PlayerDTO.model_validate(self)
			)
		)

	def player_disconnected(self):
		self.online = False
		self.add_event(
			PlayerDisconnected(
				player=PlayerDTO.model_validate(self)
			)
		)
