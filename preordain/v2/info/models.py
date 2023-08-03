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


class PriceData(BaseModel):
    scryfall_uri: str
    prices: Prices
    # set: str
    # id: str
