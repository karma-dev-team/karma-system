from typing import Any

from pydantic import BaseModel


class APIConfig(BaseModel):
    version: str = "0.0.1"
    title: str = "Karma system backend"
    description: str = "API Karma system"

    allowed_hosts: list[str] = ["*"]
    api_prefix: str = "/api"

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        return {
            # "debug": self.debug,
            # "docs_url": self.docs_url,
            "title": self.title,
            "version": self.version,
            # "default_response_class": ORJSONResponse,
            "description": self.description,
        }



