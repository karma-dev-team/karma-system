import uuid
from typing import Sequence

from sqlalchemy import Column, DateTime, func

from app.base.database.types import GUID


def id_columns() -> Sequence[Column]:
    return [
        Column("id", GUID, primary_key=True, default=uuid.uuid4, index=True, nullable=False),
    ]


def timed_columns() -> Sequence[Column]:
    return [
        Column("created_at", DateTime, server_default=func.now()),
        Column("updated_at", DateTime, onupdate=func.now(), nullable=True),
    ]

