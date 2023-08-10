import datetime
from pydantic import BaseModel
from preordain.v1.models import CardPrices, BaseResponse, BaseCardData, CardFormats
from preordain.v1.enums import CardRarity
from typing import Optional

RESP_STRING = "card_info"


class InformationData(BaseCardData):
    uri: str
    last_updated: datetime.date
    prices: CardPrices


class MetadataData(BaseCardData):
    rarity: CardRarity
    mana_cost: Optional[str]
    oracle_text: Optional[str]
    artist: Optional[str]
    legality: CardFormats


class CardInformation(BaseResponse):
    resp = RESP_STRING
    data: InformationData

    class Config:
        schema_extra = {
            "example": {
                "resp": "card_info",
                "status": 200,
                "data": {
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
                },
            }
        }
        use_enum_values = True


class CardTCGID(BaseModel):
    tcg_id: str


class CardPurchaseLink(BaseResponse):
    resp = RESP_STRING
    data: list[dict[str, CardTCGID]] = CardTCGID


class CardMetadata(BaseResponse):
    resp = RESP_STRING
    data: MetadataData
