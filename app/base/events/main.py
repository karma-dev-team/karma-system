from app.base.events.dispatcher import EventDispatcher, MemoryEventDispatcher


def configure_event_dispatcher() -> EventDispatcher:
    return MemoryEventDispatcher()
