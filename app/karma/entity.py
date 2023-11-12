from app.base.aggregate import Aggregate
from app.base.entity import entity, TimedEntity
from app.server.value_objects import ServerID


@entity
class BanEntity(Aggregate, TimedEntity):
	reason: str
	server_id: ServerID
