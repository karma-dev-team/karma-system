from attrs import field

from app.base.entity import TimedEntity, entity
from app.games.value_objects import GameID


@entity
class GameEntity(TimedEntity):
	id: GameID = field(factory=GameID.generate)
	name: str
	description: str
