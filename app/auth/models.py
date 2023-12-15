from sqlalchemy import Table, Column, String
from sqlalchemy.orm import registry as registry_class

from app.auth.entity import UserSession
from app.base.database.consts import STRING_MAX_LENGTH


def load_models(registry: registry_class):
	user_session = Table(
		"user_session",
		registry.metadata,
		Column("session_id", String(STRING_MAX_LENGTH), primary_key=True, index=True),
		Column("id", String(STRING_MAX_LENGTH)),
	)

	registry.map_imperatively(
		UserSession,
		user_session,
	)
