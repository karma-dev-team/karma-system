from attrs import field
from attrs.validators import optional, instance_of

from app.base.aggregate import Aggregate
from app.base.entity import TimedEntity, entity
from app.files.entities import PhotoEntity
from app.games.value_objects.ids import CategoryID, GameID


@entity
class CategoryEntity(Aggregate, TimedEntity):
	id: CategoryID = field(factory=CategoryID.generate)
	name: str
	game_id: GameID
	image: PhotoEntity | None = field(validator=optional(instance_of(PhotoEntity)), default=None)

	@classmethod
	def create(
		cls,
		name: str,
		game_id: GameID,
		image: PhotoEntity | None = None,
	) -> "CategoryEntity":
		cat = CategoryEntity(
			name=name,
			game_id=game_id,
			image=image,
		)

		return cat
