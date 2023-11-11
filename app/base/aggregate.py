from app.base.events.event import Event


class Aggregate:
    _events: list[Event] = []

    def get_events(self) -> list[Event]:
        if not self._events:
            self._events = []
        events = self._events.copy()
        self._events.clear()
        return events

