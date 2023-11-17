from ipaddress import IPv4Address, IPv6Address

from attrs import field

from app.base.aggregate import Aggregate
from app.base.entity import TimedEntity, entity
from app.games.value_objects.ids import GameID
from app.server.dto.server import ServerDTO
from app.server.events.server import ServerCreated
from app.server.value_objects.amount import ServerKarmaAmount
from app.server.value_objects.ids import ServerID
from app.user.entities import UserEntity
from app.user.value_objects import UserID


@entity
class ServerEntity(TimedEntity, Aggregate):
	id: ServerID = field(factory=ServerID.generate)
	name: str
	ipv4: IPv4Address
	ipv6: IPv6Address | None
	port: int
	owner: UserEntity
	owner_id: UserID
	karma: ServerKarmaAmount
	game_id: GameID

	@classmethod
	def create(
		cls,
		name: str,
		ipv4: IPv4Address,
		port: int,
		owner_id: UserID,
		game_id: UserID,
		ipv6: IPv6Address | None = None,
	) -> "ServerEntity":
		entity = ServerEntity(
			name=name,
			ipv4=ipv4,
			ipv6=ipv6,
			port=port,
			owner_id=owner_id,
			game_id=game_id,
		)

		entity.add_event(
			ServerCreated(
				server=ServerDTO.model_validate(entity)
			)
		)

		return entity
