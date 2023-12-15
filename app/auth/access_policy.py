from app.user.entities import UserEntity
from app.user.enums import UserRoles, USER_ROLES_AS_INTEGER


class BasicAccessPolicy:
    def __init__(self, user: UserEntity | None) -> None:
        self.user = user

    def anonymous(self) -> bool:
        return bool(self.user)

    @staticmethod
    def role_as_int(role: UserRoles):
        return USER_ROLES_AS_INTEGER[role.value]

    def as_int(self):
        if self.anonymous():
            return
        return USER_ROLES_AS_INTEGER[self.user.role.value]

    def check_role(self, role: UserRoles):
        if self.anonymous():
            return
        role = USER_ROLES_AS_INTEGER[role.value]
        user_role = USER_ROLES_AS_INTEGER[self.user.role]

        return role == user_role
