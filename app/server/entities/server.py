from ipaddress import IPv4Address, IPv6Address
from typing import List, Union, Optional

from attrs.validators import instance_of
from attrs import field

from app.base.aggregate import Aggregate
from app.base.entity import TimedEntity, entity
from app.games.value_objects.ids import GameID
from app.server.dto.server import ServerDTO
from app.server.entities.player import PlayerEntity
from app.server.entities.tag import ServerTagEntity
from app.server.events.server import ServerCreated, ServerRegistered
from app.karma.value_objects.karma import KarmaAmount
from app.server.value_objects.ids import ServerID
from app.user.entities import UserEntity
from app.user.value_objects import UserID


@entity
class ServerEntity(TimedEntity, Aggregate):
	id: ServerID = field(factory=ServerID.generate)
	name: str
	ipv4: IPv4Address
	ipv6: IPv6Address | None
	port: int = field(validator=instance_of(int))
	owner: UserEntity
	owner_id: UserID
	karma: KarmaAmount
	game_id: GameID
	players: List[PlayerEntity] = field(factory=list)
	tags: List[ServerTagEntity] = field(factory=list)
	registered: bool = field(default=False)

	@classmethod
	def create(
		cls,
		name: str,
		ipv4: IPv4Address,
		port: int,
		owner_id: UserID,
		game_id: GameID,
		ipv6: IPv6Address | None = None,
		tags: Optional[Union[list[ServerTagEntity], str, list]] = None,
	) -> "ServerEntity":
		if not tags:
			tags = []
		entity = ServerEntity(
			name=name,
			ipv4=ipv4,
			ipv6=ipv6,
			port=port,
			owner_id=owner_id,
			game_id=game_id,
			tags=tags,
		)
		if isinstance(tags, (str, list)):
			if isinstance(tags, str):
				names = tags.split(";")
			else:
				names = tags
			for name in names:
				entity.tags.append(
					ServerTagEntity.create(
						name=name,
						server_id=entity.id,
					)
				)

		entity.add_event(
			ServerCreated(
				server=ServerDTO.model_validate(entity)
			)
		)

		return entity

	def register(self):
		if self.registered:
			return

		self.registered = True
		self.add_event(
			ServerRegistered(
				server=ServerDTO.model_validate(self)
			)
		)
