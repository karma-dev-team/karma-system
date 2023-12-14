from typing import TYPE_CHECKING

from attrs import field
from attrs.validators import optional, instance_of

from app.base.entity import TimedEntity, entity
from app.karma.calculations import calc_ban_karma, calc_warn_karma, calc_perma_ban_karma
from app.karma.enums import KarmaRecordType
from app.karma.value_objects.ids import KarmaRecID
from app.karma.value_objects.karma import KarmaAmount
from app.server.value_objects.ids import PlayerID, ServerID
from app.user.value_objects import UserID

if TYPE_CHECKING:
    from app.server.entities.player import PlayerEntity
    from app.server.entities.server import ServerEntity


@entity
class KarmaRecordEntity(TimedEntity):
    id: KarmaRecID
    delta_karma: KarmaAmount
    player_id: PlayerID
    from_id: UserID | None = field(validator=optional(instance_of(UserID)), default=None)
    from_ply_id: PlayerID | None = field(validator=optional(instance_of(PlayerID)), default=None)
    server_id: ServerID
    reason: str | None = field(validator=instance_of(str))
    duration: int | None = field(validator=optional(instance_of(int)), default=None)  # in minutes
    type: KarmaRecordType = field(validator=instance_of(KarmaRecordType))

    @classmethod
    def create(
        cls,
        delta_karma: KarmaAmount,
        server: "ServerEntity",
        player: "PlayerEntity",
        reason: str,
    ) -> "KarmaRecordEntity":
        rec = KarmaRecordEntity(
            delta_karma=delta_karma,
            player_id=player.id,
            server_id=server.id,
            type=KarmaRecordType.change,
            reason=reason,
        )
        return rec

    @classmethod
    def create_from_ban(
        cls,
        duration: int,  # in minutes
        reason: str,
        server: "ServerEntity",
        player: "PlayerEntity",
    ) -> "KarmaRecordEntity":
        if duration == 0:
            calced_karma = calc_perma_ban_karma(server_karma=server.karma, player_karma=player.karma)
        else:
            calced_karma = calc_ban_karma(
                duration,
                server.karma,
                player.karma,
            )

        rec = KarmaRecordEntity(
            delta_karma=calced_karma,
            server_id=server.id,
            player_id=player.id,
            reason=reason,
            type=KarmaRecordType.ban,
        )

        return rec

    @classmethod
    def create_from_warn(
        cls,
        reason: str,
        server: "ServerEntity",
        player: "PlayerEntity",
    ) -> "KarmaRecordEntity":
        calced_karma = calc_warn_karma(
            server.karma,
            player.karma,
        )

        rec = KarmaRecordEntity(
            delta_karma=calced_karma,
            server_id=server.id,
            player_id=player.id,
            reason=reason,
            type=KarmaRecordType.warn,
        )

        return rec
