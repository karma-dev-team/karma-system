from app.base.dto import DTO
from app.server.dto.player import GetPlayerDTO
from app.server.value_objects.ids import ServerID


class HandleBanDTO(DTO):
    reason: str
    duration: int   # in minutes
    server_id: ServerID
    ply_id: GetPlayerDTO
