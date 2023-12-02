from app.base.uow import AbstractUoW
from app.user.interfaces import AbstractUserRepo


class AbstractUserUoW(AbstractUoW):
	user: AbstractUserRepo
