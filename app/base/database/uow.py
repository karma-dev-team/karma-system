from app.base.uow import AbstractUoW
from app.karma.interfaces.uow import AbstractKarmaUoW
from app.server.interfaces.uow import AbstractServerUoW


class SQLAlchemyUoW(AbstractUoW, AbstractServerUoW, AbstractKarmaUoW):
    pass
