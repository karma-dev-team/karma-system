from sqlalchemy import Table, Column, String, Integer, ForeignKey, Numeric, DECIMAL
from sqlalchemy.orm import registry as registry_class, relationship

from app.base.database.consts import STRING_MID_LENGTH
from app.base.database.models import id_columns, timed_columns
from app.server.entities.server import ServerEntity


def load_models(registry: registry_class):
    server = Table(
        'servers',
        registry.metadata,
        *id_columns(),
        *timed_columns(),
        Column("name", String(STRING_MID_LENGTH), nullable=False),
        Column("port", Integer, nullable=False),
        Column("ipv4", String(STRING_MID_LENGTH), nullable=False),
        Column("ipv6", String(STRING_MID_LENGTH), nullable=True),
        Column("owner_id", ForeignKey("users.id"), nullable=False),
        Column("karma", DECIMAL, nullable=False),
        Column("game_id", ForeignKey("games.id"), nullable=False),
    )

    registry.map_imperatively(
        ServerEntity,
        server,
        properties={
            "owner": relationship(
                "UserEntity",
                lazy="joined",
                uselist=False,
                join_depth=4,
            )
        }
    )
