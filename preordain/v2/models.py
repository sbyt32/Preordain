from pydantic import BaseModel, validator
import datetime
from typing import Optional


class PreordainData(BaseModel):
    pass


class PreordainInfo(BaseModel):
    pass


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

    @validator("data")
    def validate_if_data(cls, val):
        if issubclass(type(val), PreordainData):
            return val

        raise TypeError("Wrong Type for data field.")


class CardPrices(BaseModel):
    date: datetime.date | None
    usd: float | None
    usd_foil: float | None
    usd_etch: float | None
    euro: float | None
    euro_foil: float | None
    tix: float | None
