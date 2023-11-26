import abc

from app.user.interfaces import AbstractUserService


class AbstractIoContainer:
	"""
	Class to help inject dependencies into services without
	a pain, and mediator
	"""
	@abc.abstractmethod
	def user_service(self) -> AbstractUserService:
		pass
