from preordain.v2.models import PreordainData, CardPrices
from pydantic import BaseModel
import datetime


class CardMetadata(BaseModel):
    card_name: str
    set_code: str
    collector_number: str
    mana_cost: str | None
    oracle_text: str | None
    artist: str | None


class CardData(PreordainData):
    scryfall_uri: str
    card_data: CardMetadata
    prices: CardPrices
