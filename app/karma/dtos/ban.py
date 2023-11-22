from app.base.dto import DTO
from app.karma.value_objects.ids import BanID
from app.server.dto.player import GetPlayerDTO
from app.server.value_objects.ids import ServerID


class HandleBanDTO(DTO):
    reason: str
    duration: int   # in minutes
    ply_id: GetPlayerDTO


class BanDTO(DTO):
    id: BanID
    reason: str
    server_id: ServerID
    duration: int  # in minutes


