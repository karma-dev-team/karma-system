from app.base.event import event_wrapper
from app.base.events.event import Event
from app.server.dto.server import ServerDTO


@event_wrapper
class ServerCreated(Event):
	server: ServerDTO
