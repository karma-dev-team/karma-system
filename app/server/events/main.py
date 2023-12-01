from app.base.events.dispatcher import EventDispatcher
from app.server.events.player import PlayerKarmaChanged


async def handle_karma_handler(event: PlayerKarmaChanged, data: dict) -> None:
	pass


def load_event_dispatcher(event_dispatcher: EventDispatcher) -> None:
	event_dispatcher.register_domain_event(PlayerKarmaChanged, handle_karma_handler)
