from app.base.dto import DTO
from app.karma.value_objects.karma import KarmaAmount
from app.server.value_objects.ids import PlayerID
from app.user.value_objects import UserID


class ChangeKarmaDTO(DTO):
    """
    Can use only reg admin users
    """
    to_id: PlayerID
    delta: KarmaAmount
    user_id: UserID


class KarmaRecDTO(DTO):
    pass
