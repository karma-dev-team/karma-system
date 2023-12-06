from app.base.database.repo import SQLAlchemyRepo
from app.karma.interfaces.persistence import AbstractKarmaRepository


class KarmaRepoImpl(AbstractKarmaRepository, SQLAlchemyRepo):
    pass
