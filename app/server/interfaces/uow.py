from app.base.uow import AbstractUoW
from app.server.interfaces.persistance import AbstractServerRepo, AbstractPlayerRepo


class AbstractServerUoW(AbstractUoW):
	server: AbstractServerRepo
	player: AbstractPlayerRepo
