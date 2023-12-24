from app.auth.mailing.base import AbstractMailing


async def auth_lifespan(email_mailing: AbstractMailing):
    await email_mailing.configure()
