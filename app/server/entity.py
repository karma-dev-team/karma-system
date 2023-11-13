from attrs import field

from app.base.aggregate import Aggregate
from app.base.entity import TimedEntity, entity
from app.base.value_objects.ids import IPUIDValueObject
from app.server.value_objects import ServerID, ServerKarmaAmount
from app.user.entities import UserEntity
from app.user.value_objects import UserID


@entity
class ServerEntity(TimedEntity, Aggregate):
	id: ServerID = field(factory=ServerID.generate)
	name: str
	ip: IPUIDValueObject
	port: int
	owner: UserEntity
	owner_id: UserID
	karma: ServerKarmaAmount
