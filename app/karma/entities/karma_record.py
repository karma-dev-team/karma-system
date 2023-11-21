import decimal

from app.base.entity import TimedEntity, entity
from app.user.value_objects import UserID


@entity
class KarmaRecord(TimedEntity):
    id: KarmaRecID
    delta_karma: decimal.Decimal
    user_id: UserID
