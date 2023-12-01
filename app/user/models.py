from enum import Enum

from sqlalchemy import Table, Column, Enum, VARCHAR, String, Boolean
from sqlalchemy.orm import registry as registry_class

from app.base.database.consts import STRING_MID_LENGTH, STRING_EMAIL_LENGTH, STRING_MAX_LENGTH
from app.base.database.models import id_columns, timed_columns
from app.user.entities import UserEntity
from app.user.enums import UserRoles


def load_models(registry: registry_class) -> None:
	user_table = Table(
		"users",
		registry.metadata,
		*id_columns(),
		*timed_columns(),
		Column("role", Enum(UserRoles), nullable=False, default=UserRoles.user),
		Column("name", String(STRING_MID_LENGTH), nullable=False),
		Column("email", String(STRING_EMAIL_LENGTH), nullable=False),
		Column("hashed_password", String(STRING_MAX_LENGTH), nullable=False),
		Column("blocked", Boolean, default=False)
	)

	registry.map_imperatively(
		UserEntity,
		user_table,
	)
