import abc
from typing import Mapping, Any

from app.auth.dto import AskResetPasswordDTO, ResetPasswordDTO


class AbstractAuthService:
    @abc.abstractmethod
    async def reset_password(self, dto: ResetPasswordDTO):
        pass

    @abc.abstractmethod
    async def ask_reset_password(self, dto: AskResetPasswordDTO, base_url: str) -> None:
        pass

    @abc.abstractmethod
    async def verify_reset_password(self, reset_token: str) -> Mapping[str, Any]:
        pass
