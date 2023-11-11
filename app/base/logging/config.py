from pydantic import BaseModel


class LoggingConfig(BaseModel):
	path: str
	logging_level: str = "info"
	retention: str = "1 week"
	rotation: str = "20 MB"
	format: str = ("<level>{level: <8}</level> <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> "
	               "<cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>")
