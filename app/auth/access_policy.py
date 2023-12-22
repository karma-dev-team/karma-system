from app.user.entities import UserEntity
from app.user.enums import UserRoles, USER_ROLES_AS_INTEGER


class BasicAccessPolicy:
    def __init__(self, user: UserEntity | None) -> None:
        self.user = user

    def anonymous(self) -> bool:
        return not bool(self.user)

    @staticmethod
    def role_as_int(role: UserRoles):
        return USER_ROLES_AS_INTEGER[role.value]

    def as_int(self):
        if self.user.superuser:
            return USER_ROLES_AS_INTEGER[UserRoles.admin]

        if self.anonymous():
            return
        return USER_ROLES_AS_INTEGER[self.user.role.value]

    def check_role(self, *roles: UserRoles):
        if self.user.superuser:
            return True

        if self.anonymous():
            return False

        for role in roles:
            role_int = USER_ROLES_AS_INTEGER[role.value]
            user_role = USER_ROLES_AS_INTEGER[self.user.role]

            if role_int > user_role:
                return False

        return True
