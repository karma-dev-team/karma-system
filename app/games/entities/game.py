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

	@classmethod
	def create(cls, name: str, description: str, image: PhotoEntity | None) -> "GameEntity":
		return GameEntity(
			name=name,
			description=description,
		)
