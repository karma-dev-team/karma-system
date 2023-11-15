from datetime import datetime

from pydantic import BaseModel, Extra


class DTO(BaseModel):
    # от этого класса должны наследоватся все DTO
    class Config:
        use_enum_values = True
        extra = Extra.forbid
        frozen = True
        orm_mode = True


class TimedDTO(BaseModel):
    created_at: datetime
    updated_at: datetime | None 
