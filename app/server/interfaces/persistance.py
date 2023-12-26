from dataclasses import field
from ipaddress import IPv4Address, IPv6Address
from typing import Protocol, Sequence

from app.base.database.filters import filter_wrapper
from app.base.database.result import Result
from app.games.value_objects.ids import GameID, CategoryID
from app.server.dto.player import GetPlayerDTO
from app.server.entities.player import PlayerEntity
from app.server.entities.server import ServerEntity
from app.server.entities.tag import ServerTagEntity
from app.server.exceptions import ServerAlreadyExists, IPPortAlreadyTaken
from app.server.value_objects.ids import ServerID, PlayerID
from app.server.value_objects.steam_id import SteamID


@filter_wrapper
class PlayerFilter:
	steam_id: SteamID | None = field(default=None)
	ipv4: str | None = field(default=None)
	ipv6: str | None = field(default=None)
	name: str | None = field(default=None)
	player_id: PlayerID | None = field(default=None)

	@classmethod
	def from_dto(cls, dto: GetPlayerDTO) -> "PlayerFilter":
		return PlayerFilter(
			steam_id=dto.steam_id,
			ipv4=str(dto.ipv4),
			ipv6=str(dto.ipv6),
			name=dto.name,
		)


@filter_wrapper
class GetServersFilter:
	game_id: GameID | None = field(default=None)
	tags: Sequence[ServerTagEntity] | None = field(default=None)
	unregistered: bool | None = field(default=None)
	server_ids: Sequence[ServerID] | None = field(default=None)
	name: str | None = field(default=None)
	category_id: CategoryID | None = field(default=None)


@filter_wrapper
class GetServerFilter:
	name: str | None = field(default=None)
	server_id: ServerID | None = field(default=None)


class AbstractPlayerRepo(Protocol):
	async def find_by_filters(self, filter_: PlayerFilter) -> PlayerEntity | None:
		pass

	async def add_player(self, player: PlayerEntity) -> Result[PlayerEntity, None]:
		pass

	async def edit_player(self, player: PlayerEntity) -> Result[PlayerEntity, None]:
		pass


class AbstractServerRepo(Protocol):
	async def find_by_filters(self, filter_: GetServerFilter) -> ServerEntity | None:
		pass

	async def add_server(self, server: ServerEntity) -> Result[ServerEntity, ServerAlreadyExists | IPPortAlreadyTaken]:
		pass

	async def filter(self, filter: GetServersFilter) -> Sequence[ServerEntity]:
		pass

	async def update_server(self, server: ServerEntity) -> ServerEntity:
		pass
