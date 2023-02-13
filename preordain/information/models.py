import datetime
from pydantic import BaseModel
from preordain.models import CardPrices


class CardInformation(BaseModel):
    name: str
    set: str
    set_full: str
    id: str
    last_updated: datetime.date
    prices: CardPrices

    class Config:
        schema_extra = {
            "example": {
                "name": "Ancient Grudge",
                "set": "MM3",
                "set_full": "Modern Masters 2017",
                "id": "88",
                "last_updated": "2023-02-05",
                "prices": {
                    "usd": 12.34,
                    "usd_foil": 12.34,
                    "euro": 12.34,
                    "euro_foil": 12.34,
                    "tix": 12.34,
                },
            }
        }
        use_enum_values = True
