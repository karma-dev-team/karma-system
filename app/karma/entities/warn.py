from app.base.entity import TimedEntity, entity
from app.karma.value_objects.ids import WarnID
from app.server.value_objects.ids import ServerID


@entity
class WarnEntity(TimedEntity):
	id: WarnID
	reason: str
	server_id: ServerID
	max: int
	current: int
