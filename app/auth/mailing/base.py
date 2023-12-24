from abc import abstractmethod
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional, Sequence

PayloadT = MIMEText | str | EmailMessage


class AbstractMailing:
    """
    AbstractMailing class describes simple methods for sending emails.
    """
    @abstractmethod
    async def configure(self, *args, **kwargs) -> None:
        ...

    @abstractmethod
    async def send_file(self, file: MIMEMultipart) -> None:
        ...

    @abstractmethod
    async def send_message(self, payload: PayloadT, recipients: Optional[str | Sequence[str]] = None) -> None:
        ...

    @abstractmethod
    async def close(self):
        ...
