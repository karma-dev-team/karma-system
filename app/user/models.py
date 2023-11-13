from enum import Enum

from sqlalchemy import Table, Column, Enum
from sqlalchemy.orm import registry as registry_class

from app.base.database.models import id_columns, timed_columns
from app.user.entities import UserEntity
from app.user.enums import UserRoles


def load_models(registry: registry_class) -> None:
	user_table = Table(
		"users",
		registry.metadata,
		*id_columns(),
		*timed_columns(),
		Column("role", Enum(UserRoles), nullable=False),
	)

	registry.map_imperatively(
		UserEntity,
		user_table,
	)
