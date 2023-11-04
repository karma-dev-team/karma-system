from pathlib import Path
from typing import Any

import toml
from pydantic import BaseModel

from app.infrastructure.api.config import APIConfig
from app.infrastructure.database.config import DatabaseConfig
from app.infrastructure.logging.config import LoggingConfig


class GlobalConfig(BaseModel):
	db: DatabaseConfig
	logging: LoggingConfig
	api: APIConfig | None

	debug: bool = True

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
