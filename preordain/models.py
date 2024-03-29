from typing import TypeVar, Generic, Optional
from pydantic import BaseModel, validator, root_validator, Field
from pydantic.generics import GenericModel
from enum import Enum
from preordain.enums import CardFormatLegalities
import datetime
from typing import Any
from preordain.config import PROJECT


class CardPrices(BaseModel):
    usd: Optional[float] = 0.00
    usd_foil: Optional[float] = 0.00
    usd_etch: Optional[float] = None
    euro: Optional[float] = 0.00
    euro_foil: Optional[float] = 0.00
    tix: Optional[float] = 0.00


class CardPricesSingle(BaseModel):
    date: datetime.date
    usd: Optional[float] = 0.00
    usd_change: Optional[str] = "0.00%"
    usd_foil: Optional[float] = 0.00
    usd_foil_change: Optional[str] = "0.00%"
    euro: Optional[float] = 0.00
    euro_change: Optional[str] = "0.00%"
    euro_foil: Optional[float] = 0.00
    euro_foil_change: Optional[str] = "0.00%"
    tix: Optional[float] = 0.00
    tix_change: Optional[str] = "0.00%"


class BaseCardData(BaseModel):
    name: str = Field(max_length=255)
    set: str = Field(max_length=12)
    set_full: str
    id: str


class CardFormats(BaseModel):
    standard: CardFormatLegalities = Field(default=CardFormatLegalities.not_legal)
    historic: CardFormatLegalities = Field(default=CardFormatLegalities.not_legal)
    pioneer: CardFormatLegalities = Field(default=CardFormatLegalities.not_legal)
    modern: CardFormatLegalities = Field(default=CardFormatLegalities.not_legal)
    legacy: CardFormatLegalities = Field(default=CardFormatLegalities.not_legal)
    pauper: CardFormatLegalities = Field(default=CardFormatLegalities.not_legal)
    vintage: CardFormatLegalities = Field(default=CardFormatLegalities.not_legal)
    commander: CardFormatLegalities = Field(default=CardFormatLegalities.not_legal)


class RespStrings(str, Enum):
    # ! Error
    invalid_token = "invalid_token"
    error_request = "error_request"  # * For any Errors  | 400
    no_results = "no_results"  # * No results      | 404
    root_error = "root_error"  # * Access root     | 403
    validation_error = "validation_error"  # * validation_error | 422

    class Config:
        use_enum_values = True


ResponseDataTypes = TypeVar("ResponseDataTypes", list, dict)


class BaseInfo(BaseModel):
    message: str = "undefined error"


class BaseResponse(GenericModel, Generic[ResponseDataTypes]):
    def __init__(self, **data) -> None:
        super().__init__(**data)
        if self.info == None:
            del self.info
        if self.data == None:
            del self.data

    resp: str
    status: int
    info: Optional[dict]
    data: Optional[ResponseDataTypes]

    class Config:
        use_enum_values = True

    @validator("info")
    def check_for_info_or_data(cls, v, values):
        if v is None and values.get("data") is None:
            raise ValueError("must return either values and/or info")
        return v


class BaseError(GenericModel):
    resp: RespStrings
    status: int
    info: BaseInfo

    class Config:
        fields = {"__module__": {"exclude": True}, "__doc__": {"exclude": True}}
        use_enum_values = True


class RootChecks(BaseModel):
    Set_Information: bool
    PriceData: bool


class RootInfo(BaseModel):
    message: str
    checks: RootChecks


class RootResponse(BaseResponse):
    resp = "root_test"
    status = 200
    info = RootInfo

    class Config:
        schema_extra = {
            "example": {
                "resp": "root_test",
                "status": 200,
                "info": {
                    "message": "Welcome to Preordain! The following is the checks that is needed for data to show up. If any are false, that might be why nothing is displaying.",
                    "checks": {
                        "Set Information": True,
                        "Price Data (at least one days worth)": True,
                    },
                },
            }
        }
