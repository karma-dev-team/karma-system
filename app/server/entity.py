from attrs import field

from app.base.entity import TimedEntity
from app.base.value_objects.ids import IPUIDValueObject
from app.server.value_objects import ServerID


class ServerEntity(TimedEntity):
	id: ServerID = field(factory=ServerID.generate)
	name: str
	ip: IPUIDValueObject

