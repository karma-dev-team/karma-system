from app.base.exceptions import ApplicationError


class GameAlreadyExists(ApplicationError):
    def message(self) -> str:
        return "Game already exists"


class GameNotExists(ApplicationError):
    def message(self) -> str:
        return "game with given id does not exists"


class CategoryNotExists(ApplicationError):
    def message(self) -> str:
        return "category does not exists"


class GameNameAlreadyTaken(ApplicationError):
    def message(self) -> str:
        return "game name already taken by other row"


class CategoryNameAlreadyTaken(ApplicationError):
    def message(self) -> str:
        return "category name already taken by other category"
