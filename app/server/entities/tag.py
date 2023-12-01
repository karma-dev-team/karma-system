from attrs import field

from app.base.entity import TimedEntity, entity
from app.server.value_objects.ids import ServerTagID, ServerID


@entity
class ServerTagEntity(TimedEntity):
    id: ServerTagID = field(factory=ServerTagID.generate)
    name: str
    server_id: ServerID

    @classmethod
    def create(
        cls,
        name: str,
        server_id: ServerID,
    ) -> "ServerTagEntity":
        return ServerTagEntity(
            name=name,
            server_id=server_id,
        )
