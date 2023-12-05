from pydantic import BaseModel


class SecurityConfig(BaseModel):
    secret_key: str


class RedisConfig(BaseModel):
    dsn: str
