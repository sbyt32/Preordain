import datetime
from pydantic import BaseModel
from typing import Optional
from preordain.models import CardPrices, CardPricesSingle


class PriceDataMultiple(BaseModel):
    name: str
    set: str
    set_full: str
    id: str
    date: datetime.date
    prices: CardPrices

    class Config:
        schema_extra = {
            "example": {
                "name": "Ancient Grudge",
                "set": "MM3",
                "set_full": "Modern Masters 2017",
                "id": "88",
                "date": "2023-02-05",
                "prices": {
                    "usd": 12.34,
                    "usd_foil": 12.34,
                    "euro": 12.34,
                    "euro_foil": 12.34,
                    "tix": 12.34,
                },
            }
        }


class PriceDataSingle(BaseModel):
    name: str
    set: str
    set_full: str
    id: str
    prices: list[CardPricesSingle]

    class Config:
        schema_extra = {
            "example": {
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
        }
