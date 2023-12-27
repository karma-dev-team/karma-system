from pydantic import BaseModel
from pydantic.v1 import BaseSettings


class SecurityConfig(BaseModel):
    secret_key: str


class SecurityConfigOld(BaseSettings):
    secret_key: str
    token_key: str = "csrf_token"
    token_location: str = "body"


class RedisConfig(BaseModel):
    dsn: str
