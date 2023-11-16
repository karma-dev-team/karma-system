from typing import Sequence

from app.games.dto.player import PlayerDTO
from app.server.dto.server import GetPlayersKarmaDTO


class ServerService:
	async def player_karmas(self, dto: GetPlayersKarmaDTO) -> Sequence[PlayerDTO]:
		pass
