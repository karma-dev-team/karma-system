from app.base.uow import AbstractUoW
from app.files.interfaces.persistance import AbstractFileRepo


class AbstractFileUoW(AbstractUoW):
	file: AbstractFileRepo
