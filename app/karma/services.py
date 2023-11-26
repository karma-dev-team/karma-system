from app.base.events.dispatcher import EventDispatcher
from app.games.dto.player import PlayerDTO
from app.karma.calculations import calc_ban_karma
from app.karma.dtos.ban import HandleBanDTO
from app.karma.dtos.karma import ChangeKarmaDTO
from app.karma.dtos.warn import HandleWarnDTO
from app.karma.interfaces.services import AbstractKarmaService
from app.karma.interfaces.uow import AbstractKarmaUoW
from app.server.dto.server import ServerDTO
from app.server.exceptions import PlayerDoesNotExists, ServerNotExists
from app.server.interfaces.uow import AbstractServerUoW


class KarmaService(AbstractKarmaService):
	def __init__(
		self,
		uow: AbstractKarmaUoW,
		event_dispatcher: EventDispatcher,
		server_uow: AbstractServerUoW,
	):
		self.uow = uow
		self.server_uow = server_uow
		self.event_dispatcher = event_dispatcher

	async def change_karma(self, dto: ChangeKarmaDTO) -> PlayerDTO:
		pass

	async def handle_ban(self, dto: HandleBanDTO) -> PlayerDTO:
		ply = await self.server_uow.player.find_by_filters(dto.ply_id)
		if not ply:
			raise PlayerDoesNotExists()
		server = await self.server_uow.player.find_by_id(dto.server_id)
		if not server:
			raise ServerNotExists(server.id)
		delta_karma = calc_ban_karma(dto.duration, server.karma, ply.karma)
		async with self.uow.transaction():
			ply.change_karma(delta_karma)
			await self.event_dispatcher.publish_events(ply.events)

	async def handle_warn(self, dto: HandleWarnDTO) -> PlayerDTO:
		pass
