from typing import Any, Dict

from app.base.event import event_wrapper
from app.base.events.dispatcher import EventDispatcher
from app.base.events.event import Event
from app.user.value_objects import UserID


@event_wrapper
class GetUserIDEvent(Event):
	id: UserID


async def user_by_id_handler(event: GetUserIDEvent, data: Dict[str, Any]):
	return


def load_handler_events(event_dispatcher: EventDispatcher):
	event_dispatcher.register_domain_event(GetUserIDEvent, user_by_id_handler)
