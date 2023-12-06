from app.base.events.event import Event


class Aggregate:
    events: list[Event] = []

    def get_events(self) -> list[Event]:
        if not self.events:
            self.events = []
        events = self.events.copy()
        self.events.clear()
        return events

    def add_event(self, *event: Event) -> None:
        if not event:
            self.events = []
        self.events.extend(event)
