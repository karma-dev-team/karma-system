from sqlalchemy import Table, Column, String, ForeignKey, Integer, BigInteger, DECIMAL
from sqlalchemy.orm import registry as registry_class

from app.base.database.consts import STRING_MAX_LENGTH
from app.base.database.models import id_columns, timed_columns


def load_models(registry: registry_class):
    ban_record = Table(
        'karma_record',
        registry.metadata,
        *id_columns(),
        *timed_columns(),
        Column("reason", String(STRING_MAX_LENGTH), nullable=False),
        Column("duration", BigInteger, nullable=True),
        Column("delta_karma", DECIMAL),
        Column("player_id", ForeignKey("players.id"), nullable=False),
        Column("server_id", ForeignKey("servers.id"), nullable=False),
        Column("duration", Integer, nullable=False),  # in minutes
    )

    registry.map_imperatively(
        BanEntity,
        ban_record,
    )
