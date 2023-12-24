import abc

from app.auth.dto import ResetPasswordDTO


class AbstractAuthService:
    @abc.abstractmethod
    async def reset_password(self, dto: ResetPasswordDTO):
        pass
