import datetime
from pydantic import BaseModel
from typing import Optional, Union, Any
from preordain.models import CardPrices, CardPricesSingle, BaseResponse, RespStrings
from enum import Enum


class PriceData(BaseModel):
    name: str
    set: str
    set_full: str
    id: str
    date: Optional[datetime.date]
    prices: Union[CardPrices, CardPricesSingle]


class PriceDataMultiple(BaseResponse):
    resp = RespStrings.price_data
    data: list[dict[PriceData]] = PriceData

    class Config:
        schema_extra = {
            "example": {
                "resp": "price_data",
                "status": 200,
                "data": [
                    {
                        "name": "Ancient Grudge",
                        "set": "MM3",
                        "set_full": "Modern Masters 2017",
                        "id": "88",
                        "prices": {
                            "usd": 12.34,
                            "usd_foil": 12.34,
                            "euro": 12.34,
                            "euro_foil": 12.34,
                            "tix": 12.34,
                        },
                    }
                ],
            }
        }


class PriceDataSingle(BaseResponse):
    resp = RespStrings.price_data
    data: dict[PriceData] = PriceData

    class Config:
        schema_extra = {
            "example": {
                "resp": "price_data",
                "status": 200,
                "data": [
                    {
                        "name": "Ancient Grudge",
                        "set": "MM3",
                        "set_full": "Modern Masters 2017",
                        "id": "88",
                        "prices": [
                            {
                                "date": "2023-02-05",
                                "usd": 12.34,
                                "usd_change": "10.00%",
                                "usd_foil": 12.34,
                                "usd_foil_change": "10.00%",
                                "euro": 12.34,
                                "euro_change": "10.00%",
                                "euro_foil": 12.34,
                                "euro_foil_change": "10.00%",
                                "tix": 12.34,
                                "tix_change": "10.00%",
                            }
                        ],
                    }
                ],
            }
        }


class PriceChangePercent(BaseModel):
    name: str
    set: str
    set_full: str
    id: str
    date: datetime.date
    usd: Optional[float]
    usd_change: Optional[int]
    euro: Optional[float]
    euro_change: Optional[int]


class PriceChange(BaseResponse):
    resp = RespStrings.price_data
    status = 200
    data: list[dict[PriceChangePercent]] = PriceChangePercent


class GrowthDirections(str, Enum):
    ASC = "ASC"
    DESC = "DESC"


class GrowthCurrency(str, Enum):
    USD = "USD"
    Euro = "Euro"
    # USD, Euro, TIX
