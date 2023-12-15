import uuid
from typing import Sequence

from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import registry as registry_class

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


def load_all_models(registry: registry_class):
    from app.user.models import load_models as load_users
    from app.server.models import load_models as load_server
    from app.games.models import load_models as load_games
    from app.karma.models import load_models as load_karma
    from app.auth.models import load_models as load_auth

    load_users(registry)
    load_auth(registry)
    load_server(registry)
    load_games(registry)
    load_karma(registry)
