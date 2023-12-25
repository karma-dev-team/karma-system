import asyncio

from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional, Sequence

import aiosmtplib

from app.auth.mailing.base import AbstractMailing, PayloadT
from app.auth.mailing.config import MailingConfig


class YandexMailing(AbstractMailing):
    def __init__(self, sender_email: str, sender_password: str, timeout: int = 10):
        self.client = aiosmtplib.SMTP(
            hostname="smtp.yandex.ru",
            username=sender_email,
            password=sender_password,
            port=465,
            use_tls=True,
            timeout=timeout,
        )
        self.sender = sender_email
        self._configured = False

    async def configure(self) -> None:
        if self._configured:
            return
        await self.client.connect()
        self._configured = True

    async def send_message(self, payload: PayloadT, recipients: Optional[str | Sequence[str]] = None) -> None:
        if isinstance(payload, MIMEText):
            payload["From"] = self.sender + "@yandex.ru"
            await self.client.send_message(payload)
        elif isinstance(payload, EmailMessage):
            await self.client.send_message(payload, sender=self.sender)
        elif isinstance(payload, str):
            await self.client.sendmail(
                self.sender, recipients, payload)
        else:
            raise TypeError("Not supported message type")

    async def send_file(self, file: MIMEMultipart) -> None:
        await self.client.send_message(file, sender=self.sender)

    async def close(self):
        await self.client.quit()


def load_yandex_mailing(config: MailingConfig) -> YandexMailing:
    mailing = YandexMailing(
        sender_email=config.sender_email,
        sender_password=config.sender_password,
    )

    return mailing
