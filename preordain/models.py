from typing import TypeVar, Generic, Optional
from enum import Enum
from pydantic import BaseModel, validator
from pydantic.generics import GenericModel
from enum import Enum
import datetime
from typing import Any


class CardConditions(str, Enum):
    NM = "NM"
    LP = "LP"
    MP = "MP"
    HP = "HP"
    DMG = "DMG"


class CardVariants(str, Enum):
    Normal = "Normal"
    Foil = "Foil"
    Etched = "Etched"


class CardPrices(BaseModel):
    usd: Optional[float] = 0.00
    usd_foil: Optional[float] = 0.00
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


# * Generic Response & affiliates!


class RespStrings(str, Enum):
    # ! Error
    error_request = "error_request"  # * For any Errors  | 400
    no_results = "no_results"  # * No results      | 404
    root_error = "root_error"  # * Access root     | 403
    # * card/...
    card_info = "card_info"  # * /card/...
    # * search/{query}
    search_query = "search_query"  # * /search/{query}
    price_data = "price_data"  # * /price/*
    # * sales/...
    daily_card_sales = "daily_card_sales"  # * /daily/{set}/{col_num}
    recent_card_sales = "recent_card_sales"  # * /card/{tcg_id}
    # * inventory/...
    retrieve_inventory = "retrieve_inventory"  # * /inventory/...
    # * groups/...
    group_info = "group_info"  # * /groups/...


ResponseDataTypes = TypeVar("ResponseDataTypes", list, dict)


class BaseResponse(GenericModel, Generic[ResponseDataTypes]):
    resp: RespStrings
    status: int
    info: Optional[dict] = {}
    data: Optional[list[ResponseDataTypes]]

    @validator("info", pre=True)
    def check_for_info_or_data(cls, v, values):
        if v is None and values.get("data") is None:
            raise ValueError("must return either values and/or info")
        return v

    def dict(self, *args, **kwargs) -> dict[str, Any]:
        """
        Automaticaly exclude None values. Replaces regular model.dict()
        """
        kwargs.pop("exclude_defaults", None)
        return super().dict(*args, exclude_defaults=True, **kwargs)

    # class Config:
    #         title = 'Primary Response'
    # schema_extra = {
    #     "example": {
    #         "resp": "card_info",
    #         "status": 200,

    #     }
    # }
