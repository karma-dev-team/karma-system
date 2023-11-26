from app.base.event import event_wrapper
from app.games.dto.player import PlayerDTO
from app.karma.value_objects.karma import KarmaAmount


@event_wrapper
class KarmaChanged:
	ply: PlayerDTO
	delta_karma: KarmaAmount
