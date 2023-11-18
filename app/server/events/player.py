from app.base.event import event_wrapper
from app.base.events.event import Event
from app.games.dto.player import PlayerDTO


@event_wrapper
class PlayerCreated(Event):
	player: PlayerDTO
