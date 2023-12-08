from app.base.dto import DTO
from app.server.dto.player import GetPlayerDTO


class HandleBanRequest(DTO):
    reason: str
    duration: int   # in minutes
    player_id: GetPlayerDTO


class HandleWarnRequest(DTO):
    reason: str
    player_id: GetPlayerDTO

