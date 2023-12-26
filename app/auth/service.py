
from email.mime.text import MIMEText
from typing import Mapping, Any

from app.auth.dto import AskResetPasswordDTO, ResetPasswordDTO
from app.auth.exceptions import AccessDenied
from app.auth.interfaces import AbstractAuthService
from app.auth.mailing.base import AbstractMailing
from app.base.config import GlobalConfig
from app.base.events.dispatcher import EventDispatcher
from app.server.security import generate_jwt, decode_jwt
from app.user.exceptions import UserDoesNotExists
from app.user.interfaces.persistance import GetUserFilter
from app.user.interfaces.uow import AbstractUserUoW


class AuthService(AbstractAuthService):
    def __init__(
        self,
        uow: AbstractUserUoW,
        event_dispatcher: EventDispatcher,
        email_adapter: AbstractMailing,
        config: GlobalConfig,
    ):
        self.config = config
        self.uow = uow
        self.event_dispatcher = event_dispatcher
        self.email_adapter = email_adapter

    async def ask_reset_password(self, dto: AskResetPasswordDTO, base_url: str):
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
        reset_id = generate_jwt(
            data={
                'email': user.email,
                "id": str(user.id),
            },
            secret=self.config.security.secret_key,
        )
        payload = MIMEText(f"""press this link to reset your password: {base_url}/auth/password_reset/{reset_id}""")

        payload['Subject'] = 'Test mail'
        payload['To'] = user.email

        await self.email_adapter.send_message(payload=payload)

    async def verify_reset_password(self, reset_token: str) -> Mapping[str, Any]:
        data = decode_jwt(reset_token, self.config.security.secret_key)
        if not data:
            raise AccessDenied()

        user = await self.uow.user.get_user_by_filters(GetUserFilter(
            user_id=data['id'],
            email=data['email'],
        ))
        if not user:
            raise AccessDenied()
        return data

    async def reset_password(self, dto: ResetPasswordDTO):
        data = await self.verify_reset_password(dto.reset_token)

        user = await self.uow.user.get_user_by_id(data['id'])
        async with self.uow.transaction():
            user.change_password(dto.p)
            await self.uow.user.update_user(user)
            await self.event_dispatcher.publish_events(user.get_events())
