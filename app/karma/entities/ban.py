from app.base.aggregate import Aggregate
from app.base.entity import entity, TimedEntity
from app.karma.value_objects.ids import BanID
from app.server.value_objects.ids import ServerID


@entity
class BanEntity(Aggregate, TimedEntity):
	id: BanID
	reason: str
	server_id: ServerID
	duration: int  # in minutes
