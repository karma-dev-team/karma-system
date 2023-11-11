from abc import abstractmethod
from typing import List, Type

from app.base.events.event import Event
from app.base.events.observer import Handler, Observer
from app.base.logging.logger import get_logger



class EventDispatcher:
    @abstractmethod
    async def publish_events(self, events: List[Event]):
        pass

    @abstractmethod
    async def publish_notifications(self, events: List[Event]):
        pass

    @abstractmethod
    def register_domain_event(self, event_type: Type[Event], handler: Handler):
        pass

    @abstractmethod
    def register_notify(self, event_type: Type[Event], handler: Handler):
        pass


class MemoryEventDispatcher(EventDispatcher):
    def __init__(self, **data):
        self.domain_events = Observer()
        self.notifications = Observer()
        self.data = data

    async def publish_events(self, events: List[Event]):
        await self.domain_events.notify(events, data=self.data.copy())

    async def publish_notifications(self, events: List[Event]):
        await self.notifications.notify(events, data=self.data.copy())

    def register_domain_event(self, event_type: Type[Event], handler: Handler):
        self.domain_events.register(event_type, handler)

    def register_notify(self, event_type: Type[Event], handler: Handler):
        self.notifications.register(event_type, handler)


class NoopEventDispatcher(EventDispatcher):
    """
    Used for data importers.
    """
    def __init__(self, logger=None):
        self.logger = logger or get_logger()

    async def publish_events(self, events: List[Event]):
        self.logger.info("publishing events:", events)

    async def publish_notifications(self, events: List[Event]):
        self.logger.info("publishing notifications:", events)

    async def register_notify(self, event_type: Type[Event], handler: Handler):
        pass

    async def register_domain_event(self, event_type: Type[Event], handler: Handler):
        pass
