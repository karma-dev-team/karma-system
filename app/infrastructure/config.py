from pydantic import BaseModel

from app.infrastructure.database.config import DatabaseConfig
from app.infrastructure.logging.config import LoggingConfig


class GlobalConfig(BaseModel):
	db: DatabaseConfig
	logging: LoggingConfig
