import abc

from app.games.dto.player import PlayerDTO
from app.karma.dtos.ban import HandleBanDTO
from app.karma.dtos.karma import DecreaseKarmaDTO, IncreaseKarmaDTO
from app.karma.dtos.warn import HandleWarnDTO


class AbstractKarmaService:
	@abc.abstractmethod
	async def decrease_karma(self, dto: DecreaseKarmaDTO) -> PlayerDTO:
		pass

	@abc.abstractmethod
	async def increase_karma(self, dto: IncreaseKarmaDTO) -> PlayerDTO:
		pass

	@abc.abstractmethod
	async def handle_ban(self, dto: HandleBanDTO) -> PlayerDTO:
		pass

	@abc.abstractmethod
	async def handle_warn(self, dto: HandleWarnDTO) -> PlayerDTO:
		pass
