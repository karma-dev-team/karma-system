from __future__ import annotations
from typing import TYPE_CHECKING
import abc

from app.files.interfaces.services import FileService

if TYPE_CHECKING:
	# новые интерфейсы добавляй тут!
	from app.auth.interfaces import AbstractAuthService
	from app.games.interfaces.service import AbstractGameService, AbstractCategoryService
	from app.server.interfaces.service import AbstractServerService, AbstractPlayerService
	from app.karma.interfaces.services import AbstractKarmaService
	from app.user.interfaces import AbstractUserService


class AbstractIoContainer:
	"""
	Class to help inject dependencies into services without
	a pain, and mediator
	"""
	@abc.abstractmethod
	def user_service(self) -> AbstractUserService:
		pass

	@abc.abstractmethod
	def karma_service(self) -> AbstractKarmaService:
		pass

	@abc.abstractmethod
	def server_service(self) -> AbstractServerService:
		pass

	@abc.abstractmethod
	def player_service(self) -> AbstractPlayerService:
		pass

	@abc.abstractmethod
	def game_service(self) -> AbstractGameService:
		pass

	@abc.abstractmethod
	def category_service(self) -> AbstractCategoryService:
		pass

	@abc.abstractmethod
	def file_service(self) -> FileService:
		pass

	@abc.abstractmethod
	def auth_service(self) -> AbstractAuthService:
		pass
