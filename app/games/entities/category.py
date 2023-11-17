from attrs import field

from app.base.aggregate import Aggregate
from app.base.entity import TimedEntity, entity
from app.games.value_objects.ids import CategoryID, GameID


@entity
class CategoryEntity(Aggregate, TimedEntity):
	id: CategoryID = field(factory=CategoryID.generate)
	name: str
	game_id: GameID
