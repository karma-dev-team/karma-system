from attrs import field
from attrs.validators import optional, instance_of

from app.base.entity import TimedEntity, entity
from app.karma.value_objects.ids import KarmaRecID
from app.karma.value_objects.karma import KarmaAmount
from app.server.value_objects.ids import PlayerID, ServerID
from app.user.value_objects import UserID


@entity
class KarmaRecord(TimedEntity):
    id: KarmaRecID
    delta_karma: KarmaAmount
    player_id: PlayerID
    from_id: UserID | None = field(validator=optional(instance_of(UserID)))
    server_id: ServerID

    @classmethod
    def create(
        cls,
        delta_karma: KarmaAmount,
        player_id: PlayerID,
        server_id: ServerID,
    ) -> "KarmaRecord":
        rec = KarmaRecord(
            delta_karma=delta_karma,
            player_id=player_id,
            server_id=server_id,
        )

        return rec
