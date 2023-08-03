from pydantic import BaseModel, Extra
from preordain.v2.schema import PriceTable
import datetime


class Prices(BaseModel):
    date: datetime.date | None
    usd: float | None
    usd_foil: float | None
    usd_etch: float | None
    euro: float | None
    euro_foil: float | None
    tix: float | None


class CardMetadata(BaseModel):
    card_name: str
    set_code: str
    collector_number: str
    mana_cost: str | None
    oracle_text: str | None
    artist: str | None


class PriceData(BaseModel):
    scryfall_uri: str
    card_data: CardMetadata
    prices: Prices
    # set: str
    # id: str
