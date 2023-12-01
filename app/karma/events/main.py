from app.base.events.dispatcher import EventDispatcher
from app.karma.events.karma import KarmaChanged, handle_karma_change


def load_handler_events(event_dispatcher: EventDispatcher):
    event_dispatcher.register_domain_event(KarmaChanged, handle_karma_change)
