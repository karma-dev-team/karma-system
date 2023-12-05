from app.base.uow import AbstractUoW
from app.karma.interfaces.persistence import AbstractKarmaRepository


class AbstractKarmaUoW(AbstractUoW):
    karma: AbstractKarmaRepository
