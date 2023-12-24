from app.auth.dto import ResetPasswordDTO
from app.auth.interfaces import AbstractAuthService
from app.auth.mailing.base import AbstractMailing
from app.base.events.dispatcher import EventDispatcher
from app.user.exceptions import UserDoesNotExists
from app.user.interfaces.persistance import GetUserFilter
from app.user.interfaces.uow import AbstractUserUoW


class AuthService(AbstractAuthService):
    def __init__(self, uow: AbstractUserUoW, event_dispatcher: EventDispatcher, email_adapter: AbstractMailing):
        self.uow = uow
        self.event_dispatcher = event_dispatcher
        self.email_adapter = email_adapter

    async def ask_reset_password(self, dto: ResetPasswordDTO):
        """
        Returns None because it sends email to specified email
        """
        user = await self.uow.user.get_user_by_filters(
            GetUserFilter(
                email=dto.email,
            )
        )
        if not user:
            raise UserDoesNotExists(dto.email)
        self.email_adapter()
