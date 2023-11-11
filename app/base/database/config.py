from pydantic import BaseModel


class DatabaseConfig(BaseModel):
	database_dsn: str
