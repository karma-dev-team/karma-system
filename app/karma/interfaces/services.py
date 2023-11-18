import abc

from app.games.dto.player import PlayerDTO


class AbstractKarmaService:
	@abc.abstractmethod
	async def decrease_karma(self, dto: DescreaseKarmaDTO) -> PlayerDTO:
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