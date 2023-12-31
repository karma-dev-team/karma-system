from typing import TYPE_CHECKING

from app.base.event import event_wrapper
from app.base.events.event import Event
from app.server.dto.player import PlayerDTO

if TYPE_CHECKING:
	from app.karma.value_objects.karma import KarmaAmount


@event_wrapper
class PlayerKarmaChanged(Event):
	ply: PlayerDTO
	delta_karma: "KarmaAmount"


@event_wrapper
class PlayerCreated(Event):
	player: PlayerDTO


@event_wrapper
class PlayerConnected(Event):
	player: PlayerDTO


@event_wrapper
class PlayerDisconnected(Event):
	player: PlayerDTO
