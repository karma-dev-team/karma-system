from app.user.entities import UserEntity


class BasicAccessPolicy:
    def __init__(self, user: UserEntity) -> None:
        self.user = user

    def role(self):
        pass
