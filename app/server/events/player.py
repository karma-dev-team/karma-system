from app.base.event import event_wrapper
from app.base.events.event import Event
from app.games.dto.player import PlayerDTO
from app.karma.value_objects.karma import KarmaAmount


@event_wrapper
class PlayerKarmaChanged(Event):
	ply: PlayerDTO
	delta_karma: KarmaAmount


@event_wrapper
class PlayerCreated(Event):
	player: PlayerDTO
