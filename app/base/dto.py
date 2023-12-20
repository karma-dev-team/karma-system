from datetime import datetime

from pydantic import BaseModel, Extra, Field


class DTO(BaseModel):
    # от этого класса должны наследоватся все DTO
    class Config:
        use_enum_values = True
        extra = Extra.forbid
        frozen = True
        from_attributes = True


class TimedDTO(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(default=None)
