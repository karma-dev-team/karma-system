import abc

from app.auth.dto import AskResetPasswordDTO


class AbstractAuthService:
    @abc.abstractmethod
    async def reset_password(self, dto: AskResetPasswordDTO):
        pass
