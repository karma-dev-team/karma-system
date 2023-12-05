from app.base.exceptions import ApplicationError


class GameAlreadyExists(ApplicationError):
    def message(self) -> str:
        return "Game already exists"


class GameNotExists(ApplicationError):
    def message(self) -> str:
        return "game with given id does not exists"
