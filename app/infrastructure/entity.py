from datetime import datetime

from attrs import define, field

from app.infrastructure.events.event import Event

entity = define(kw_only=True, slots=False)


class Aggregate:
    _events: list[Event] = []

    def get_events(self) -> list[Event]:
        if not self._events:
            self._events = []
        events = self._events.copy()
        self._events.clear()
        return events


@entity
class TimedEntity:
    # add up this only it's required, because created_at's will be rewritten
    # by python's datetime, which will cause time conflicts.
    created_at: datetime = field(factory=datetime.now)
    updated_at: datetime = field(factory=datetime.now)
