from app.base.dto import DTO
from app.karma.enums import KarmaRecordType
from app.karma.value_objects.ids import KarmaRecID
from app.karma.value_objects.karma import KarmaAmount
from app.server.value_objects.ids import PlayerID, ServerID
from app.user.value_objects import UserID


class ChangeKarmaDTO(DTO):
    """
    Can use only reg admin users
    """
    to_id: PlayerID
    delta: KarmaAmount
    user_id: UserID


class KarmaRecDTO(DTO):
    id: KarmaRecID
    delta_karma: KarmaAmount
    player_id: PlayerID
    from_id: UserID | None
    from_ply_id: PlayerID | None
    server_id: ServerID
    reason: str | None
    duration: int | None
    type: KarmaRecordType
