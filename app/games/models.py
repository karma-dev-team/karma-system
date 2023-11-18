from sqlalchemy import Table, Column, String, ForeignKey
from sqlalchemy.orm import registry as registry_class

from app.base.database.consts import STRING_MID_LENGTH, STRING_MAX_LENGTH
from app.base.database.models import id_columns, timed_columns
from app.games.entities.category import CategoryEntity
from app.games.entities.game import GameEntity


def load_models(registry: registry_class):
	game_table = Table(
		'games',
		registry.metadata,
		*id_columns(),
		*timed_columns(),
		Column("name", String(STRING_MID_LENGTH)),
		Column("description", String(STRING_MAX_LENGTH)),
	)

	registry.map_imperatively(GameEntity, game_table)

	category_table = Table(
		'categories',
		registry.metadata,
		*id_columns(),
		*timed_columns(),
		Column("name", String(STRING_MID_LENGTH), nullable=False),
		Column("game_id", ForeignKey("GameEntity.id"), nullable=False),
	)

	registry.map_imperatively(CategoryEntity, category_table)
