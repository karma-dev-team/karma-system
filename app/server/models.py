from sqlalchemy import Table, Column, String, Integer, ForeignKey, DECIMAL, Boolean
from sqlalchemy.orm import registry as registry_class, relationship

from app.base.database.consts import STRING_MID_LENGTH, STRING_MIN_LENGTH, STRING_MAX_LENGTH
from app.base.database.models import id_columns, timed_columns
from app.server.entities.player import PlayerEntity
from app.server.entities.server import ServerEntity
from app.server.entities.tag import ServerTagEntity


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
        Column("karma", DECIMAL, default=.0),
        Column("game_id", ForeignKey("games.id"), nullable=False),
        Column("country_code", String(STRING_MIN_LENGTH), nullable=False)
    )

    server_tags = Table(
        'server_tags',
        registry.metadata,
        *id_columns(),
        *timed_columns(),
        Column("name", String(STRING_MIN_LENGTH), nullable=False),
        Column("server_id", ForeignKey("servers.id"), nullable=False),
    )

    player = Table(
        'players',
        registry.metadata,
        *id_columns(),
        *timed_columns(),
        Column("name", String(STRING_MID_LENGTH), nullable=False),
        Column("steam_id", String(STRING_MAX_LENGTH), nullable=False),
        Column("ipv4", String(STRING_MID_LENGTH), nullable=False),
        Column("ipv6", String(STRING_MAX_LENGTH), nullable=True),
        Column("hours", DECIMAL, default=0),
        Column("karma", DECIMAL, default=0),
        Column("online", Boolean, default=False),
    )

    registry.map_imperatively(
        ServerEntity,
        server,
        properties={
            'tags': relationship(
                'ServerTagEntity',
                lazy="joined"
            ),
        }
    )

    registry.map_imperatively(
        PlayerEntity,
        player,
    )

    registry.map_imperatively(
        ServerTagEntity,
        server_tags,
    )
