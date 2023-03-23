import datetime
from pydantic import BaseModel
from preordain.models import CardPrices, BaseResponse, CardInfoData
from typing import Optional

RESP_STRING = card_info = "card_info"


class CardInformation(BaseResponse):
    resp = RESP_STRING
    data: list[CardInfoData]

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
    resp = RESP_STRING
    data: list[dict[str, CardTCGID]] = CardTCGID
