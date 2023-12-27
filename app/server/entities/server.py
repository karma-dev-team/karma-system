from ipaddress import IPv4Address, IPv6Address
from typing import List, Union, Optional

from attr.validators import optional
from attrs.validators import instance_of
from attrs import field

from app.base.aggregate import Aggregate
from app.base.entity import TimedEntity, entity
from app.files.entities import PhotoEntity
from app.games.entities.game import GameEntity
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
	ipv4: str
	ipv6: str | None
	port: int = field(validator=instance_of(int))
	owner: UserEntity = field(validator=optional(instance_of(UserEntity)), default=None)
	owner_id: UserID
	karma: KarmaAmount = field(validator=instance_of(KarmaAmount), default=KarmaAmount(0))
	game_id: GameID
	game: GameEntity = field(validator=instance_of(GameEntity))
	players: List[PlayerEntity] = field(factory=list)
	tags: List[ServerTagEntity] = field(factory=list)
	registered: bool = field(default=False)
	country_code: str = field(default="RU")
	icon: PhotoEntity = field(default=None, validator=optional(instance_of(PhotoEntity)))
	discord_link: str | None = field(default=None, validator=optional(instance_of(str)))
	website_link: str | None = field(default=None, validator=optional(instance_of(str)))

	@classmethod
	def create(
		cls,
		name: str,
		ipv4: IPv4Address,
		port: int,
		owner: UserEntity,
		game: GameEntity,
		ipv6: IPv6Address | None = None,
		tags: Optional[Union[list[ServerTagEntity], str, list]] = None,
		icon: Optional[PhotoEntity] = None,
		discord_link: str | None = None,
		website_link: str | None = None,
	) -> "ServerEntity":
		entity = ServerEntity(
			name=name,
			ipv4=str(ipv4),
			ipv6=str(ipv6),
			port=port,
			owner_id=owner.id,
			owner=owner,
			game_id=game.id,
			game=game,
			icon=icon,
			discord_link=discord_link,
			website_link=website_link,
		)

		if isinstance(tags, (str, list)):
			# обработка всех тегов включая уже созданных
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
