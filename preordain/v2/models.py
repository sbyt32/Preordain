from pydantic import field_validator, ConfigDict, BaseModel, validator
import datetime
from typing import Optional


class PreordainData(BaseModel):
    pass


# class PreordainInfo(BaseModel):
#     pass


class PreordainResponse(BaseModel):
    resp: str
    status: int
    info: Optional[dict] = None
    data: Optional[list | dict] = None
    model_config = ConfigDict(use_enum_values=True)

    # Makes sure that either info or data is returned.
    # TODO[pydantic]: We couldn't refactor the `validator`, please replace it by `field_validator` manually.
    # Check https://docs.pydantic.dev/dev-v2/migration/#changes-to-validators for more information.
    @validator("info")
    def check_for_info_or_data(cls, v, values):
        if v is None and values.get("data") is None:
            raise ValueError("must return either values and/or info")
        return v

    @field_validator("data")
    @classmethod
    def validate_if_data(cls, val):
        if issubclass(type(val), PreordainData):
            return val

        raise TypeError("Wrong Type for data field.")


class CardPrices(BaseModel):
    def __init__(self, **data) -> None:
        super().__init__(**data)
        if self.date == None:
            del self.date

    date: datetime.date | None = None
    usd: float | None = None
    usd_foil: float | None = None
    usd_etch: float | None = None
    euro: float | None = None
    euro_foil: float | None = None
    tix: float | None = None
