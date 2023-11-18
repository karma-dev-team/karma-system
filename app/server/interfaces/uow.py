from app.base.uow import AbstractUoW


class AbstractServerUoW(AbstractUoW):
	server: AbstractServerRepo
	player: AbstractPlayerRepo
