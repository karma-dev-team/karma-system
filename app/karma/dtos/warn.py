from app.base.dto import DTO
from app.server.dto.player import GetPlayerDTO
from app.server.value_objects.ids import ServerID


class HandleWarnDTO(DTO):
    reason: str
    server_id: ServerID
    ply_id: GetPlayerDTO
