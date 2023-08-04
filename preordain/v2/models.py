from pydantic import BaseModel, validator
from typing import Optional


class PreordainResponse(BaseModel):
    resp: str
    status: int
    info: Optional[dict]
    data: Optional[list | dict]

    class Config:
        use_enum_values = True

    # Makes sure that either info or data is returned.
    @validator("info")
    def check_for_info_or_data(cls, v, values):
        if v is None and values.get("data") is None:
            raise ValueError("must return either values and/or info")
        return v
