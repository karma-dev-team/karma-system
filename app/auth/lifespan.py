from typing import Any

from aiosmtplib import SMTPConnectTimeoutError
from fastapi import FastAPI

from app.auth.mailing.base import AbstractMailing


async def init_mailing(app: FastAPI, workflow_data: dict[str, Any]):
    email_adapter: AbstractMailing = workflow_data['email_adapter']
    try:
        await email_adapter.configure()
    except SMTPConnectTimeoutError:
        workflow_data["logger"].error("Yandex mailing failed to initialize")


async def shutdown_mailing(app: FastAPI, workflow_data: dict[str, Any]):
    email_adapter: AbstractMailing = workflow_data['email_adapter']
    await email_adapter.close()
