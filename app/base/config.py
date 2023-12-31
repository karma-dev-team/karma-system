from pathlib import Path

import toml
from pydantic import BaseModel

from app.auth.config import SecurityConfig, RedisConfig
from app.auth.mailing.config import MailingConfig
from app.base.api.config import APIConfig
from app.base.database.config import DatabaseConfig
from app.base.logging.config import LoggingConfig


class GlobalConfig(BaseModel):
	db: DatabaseConfig
	logging: LoggingConfig
	api: APIConfig | None
	security: SecurityConfig
	redis: RedisConfig | None
	mailing: MailingConfig

	debug: bool = True
	host: str = "localhost"

	class Config:
		validate_assignment = True


def load_config(path: str | Path) -> GlobalConfig:
	"""
	loads only one time
	use DI to get actual instance of config
	"""
	if isinstance(path, str):
		path = Path(path)

	with path.open("r", encoding="utf8") as file:
		s = file.read()
		data = toml.loads(s)

	return GlobalConfig(**data)
