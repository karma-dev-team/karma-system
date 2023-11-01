from sqlalchemy import Table, Column, Integer
from sqlalchemy.orm import registry as registry_class

from app.user.entities import UserEntity


def load_models(registry: registry_class) -> None:
	user_table = Table(
		"users",
		registry.metadata,
		Column("id", Integer, primary_key=True, index=True)
	)

	registry.map_imperatively(
		UserEntity,
		user_table,
	)
