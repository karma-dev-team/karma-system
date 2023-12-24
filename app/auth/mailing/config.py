from pydantic import BaseModel


class MailingConfig(BaseModel):
    sender_email: str
    sender_password: str
