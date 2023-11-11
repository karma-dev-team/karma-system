from datetime import datetime

from attrs import define, field

from app.base.events.event import Event

entity = define(kw_only=True, slots=False)


@entity
class TimedEntity:
    # add up this only it's required, because created_at's will be rewritten
    # by python's datetime, which will cause time conflicts.
    created_at: datetime = field(factory=datetime.now)
    updated_at: datetime = field(factory=datetime.now)