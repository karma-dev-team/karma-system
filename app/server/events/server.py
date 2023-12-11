from datetime import datetime

from attr import field

from app.base.event import event_wrapper
from app.base.events.event import Event
from app.server.dto.server import ServerDTO


@event_wrapper
class ServerCreated(Event):
	server: ServerDTO


@event_wrapper
class ServerRegistered(Event):
	server: ServerDTO
	created_at: datetime = field(factory=datetime.now)
