from app.games.dto.player import PlayerDTO
from app.karma.dtos.ban import HandleBanDTO
from app.karma.dtos.karma import IncreaseKarmaDTO, DecreaseKarmaDTO
from app.karma.dtos.warn import HandleWarnDTO
from app.karma.interfaces.services import AbstractKarmaService


class KarmaService(AbstractKarmaService):
	async def decrease_karma(self, dto: DecreaseKarmaDTO) -> PlayerDTO:
		pass

	async def increase_karma(self, dto: IncreaseKarmaDTO) -> PlayerDTO:
		pass

	async def handle_ban(self, dto: HandleBanDTO) -> PlayerDTO:
		pass

	async def handle_warn(self, dto: HandleWarnDTO) -> PlayerDTO:
		pass

