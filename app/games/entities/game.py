from attrs.validators import optional, instance_of
from attrs import field

from app.base.entity import TimedEntity, entity
from app.files.entities import PhotoEntity
from app.games.value_objects.ids import GameID


@entity
class GameEntity(TimedEntity):
	id: GameID = field(factory=GameID.generate)
	name: str
	description: str
	image: PhotoEntity | None = field(validator=optional(instance_of(PhotoEntity)))
