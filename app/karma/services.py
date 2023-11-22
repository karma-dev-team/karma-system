from app.games.dto.player import PlayerDTO
from app.karma.dtos.ban import HandleBanDTO
from app.karma.dtos.karma import ChangeKarmaDTO
from app.karma.dtos.warn import HandleWarnDTO
from app.karma.interfaces.services import AbstractKarmaService


class KarmaService(AbstractKarmaService):
	async def change_karma(self, dto: ChangeKarmaDTO) -> PlayerDTO:
		pass

	async def handle_ban(self, dto: HandleBanDTO) -> PlayerDTO:
		pass

	async def handle_warn(self, dto: HandleWarnDTO) -> PlayerDTO:
		pass
