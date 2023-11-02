from app.infrastructure.event import event_wrapper
from app.infrastructure.events.dispatcher import EventDispatcher
from app.infrastructure.value_objects.ids import UIDValueObject


@event_wrapper
class GetUserIDEvent:
	id: UIDValueObject


async def user_by_id_handler(event: GetUserIDEvent):
	pass


def load_handler_events(event_dispatcher: EventDispatcher):
	event_dispatcher.register_domain_event(GetUserIDEvent, user_by_id_handler)
