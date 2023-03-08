import datetime
from pydantic import BaseModel
from preordain.models import CardPrices, BaseResponse, RespStrings
from typing import Optional


class CardInfoData(BaseModel):
    name: str
    set: str
    set_full: str
    id: str
    last_updated: datetime.date
    prices: CardPrices


class CardInformation(BaseResponse):
    resp = RespStrings.card_info
    data: list[dict[str, CardInfoData]] = CardInfoData

    class Config:
        schema_extra = {
            "example": {
                "resp": "card_info",
                "status": 200,
                "data": [
                    {
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
                ],
            }
        }
        use_enum_values = True


class CardTCGID(BaseModel):
    tcg_id: str


class CardPurchaseLink(BaseResponse):
    resp = RespStrings.card_info
    data: list[dict[str, CardTCGID]] = CardTCGID
