import logging
from typing import Tuple

from pydantic import BaseModel


class LoggingConfig(BaseModel):
	path: str
	logging_level: str = "info"  # should be in lowercase, otherwise uvicorn error
	retention: str = "1 week"
	rotation: str = "20 MB"
