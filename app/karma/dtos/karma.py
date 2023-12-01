from typing import Any

from pydantic import model_validator

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


class KarmaRecordDTO(DTO):
    id: KarmaRecID
    delta_karma: KarmaAmount
    player_id: PlayerID
    from_id: UserID | None
    from_ply_id: PlayerID | None
    server_id: ServerID
    reason: str | None
    duration: int | None
    type: KarmaRecordType

    @model_validator(mode="before")
    @classmethod
    def validate_by_type(cls, data: Any):
        """Validates to save consistency in entities"""
        if isinstance(data, dict):
            match data.get("type"):
                case KarmaRecordType.ban:
                    assert (
                        'reason' not in data and
                        'duration' not in data
                    ), 'No reason and duration are provided'
                case KarmaRecordType.warn:
                    assert (
                        'reason' not in data or
                        'duration' in data
                    ), 'Reason is not provided or/and' \
                       ' duration is provided'
                case KarmaRecordType.change:
                    assert (
                        'reason' not in data
                    ), 'Reason is not provided'

        return data
