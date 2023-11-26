from ipaddress import IPv4Address, IPv6Address
from typing import Protocol

from app.base.database.filters import filter_wrapper
from app.base.database.result import Result
from app.server.entities.player import PlayerEntity
from app.server.entities.server import ServerEntity
from app.server.value_objects.ids import ServerID
from app.server.value_objects.steam_id import SteamID


@filter_wrapper
class PlayerFilter:
	steam_id: SteamID | None
	ipv4: IPv4Address | None
	ipv6: IPv6Address | None
	name: str | None


class AbstractPlayerRepo(Protocol):
	async def find_by_filters(self, filter_: PlayerFilter) -> PlayerEntity | None:
		pass

	async def add_player(self, player: PlayerEntity) -> Result[PlayerEntity, None]:
		pass


class AbstractServerRepo(Protocol):
	async def find_by_id(self, server_id: ServerID) -> ServerEntity | None:
		pass
