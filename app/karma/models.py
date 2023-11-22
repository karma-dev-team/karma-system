from sqlalchemy import Table, Column, String, ForeignKey, Integer
from sqlalchemy.orm import registry as registry_class

from app.base.database.consts import STRING_MAX_LENGTH
from app.base.database.models import id_columns, timed_columns
from app.karma.entities.ban import BanEntity
from app.karma.entities.warn import WarnEntity


def load_models(registry: registry_class):
    ban_record = Table(
        'ban_records',
        registry.metadata,
        *id_columns(),
        *timed_columns(),
        Column("reason", String(STRING_MAX_LENGTH), nullable=False),
        Column("player_id", ForeignKey("players.id"), nullable=False),
        Column("server_id", ForeignKey("servers.id"), nullable=False),
        Column("duration", Integer, nullable=False),  # in minutes
    )

    warn_record = Table(
        'warn_records',
        registry.metadata,
        *id_columns(),
        *timed_columns(),
        Column("reason", String(STRING_MAX_LENGTH), nullable=False),
        Column("player_id", ForeignKey("players.id"), nullable=False),
        Column("server_id", ForeignKey("servers.id"), nullable=False),
    )

    registry.map_imperatively(
        BanEntity,
        ban_record,
    )

    registry.map_imperatively(
        WarnEntity,
        warn_record,
    )
