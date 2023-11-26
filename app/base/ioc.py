from __future__ import annotations
from typing import TYPE_CHECKING
import abc

if TYPE_CHECKING:
	# новые интерфейсы добавляй тут!
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
