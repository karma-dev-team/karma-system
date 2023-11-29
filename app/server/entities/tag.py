from app.base.entity import TimedEntity, entity
from app.server.value_objects.ids import ServerTagID, ServerID


@entity
class ServerTagEntity(TimedEntity):
    id: ServerTagID
    name: str
    server_id: ServerID
