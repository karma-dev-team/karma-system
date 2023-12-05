from app.base.database.result import Result
from app.user.entities import UserEntity
from app.user.exceptions import EmailAlreadyTaken, UserAlreadyExists, RegistrationCodeIsNotCorrect
from app.user.interfaces import AbstractUserRepo
from app.user.interfaces.persistance import GetUserFilter
from app.user.value_objects import UserID


class UserRepoImpl(AbstractUserRepo):
    async def get_user_by_id(self, user_id: UserID) -> UserEntity | None:
        pass

    async def get_user_by_filters(self, filter: GetUserFilter) -> UserEntity | None:
        pass

    async def add_user(
            self, user: UserEntity, reg_code: str
    ) -> Result[UserEntity, EmailAlreadyTaken | UserAlreadyExists | RegistrationCodeIsNotCorrect]:
        pass
