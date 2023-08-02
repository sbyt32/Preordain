from pydantic import BaseModel
import datetime


class PriceData(BaseModel):
    scryfall_uri: str
    # set: str
    # id: str
    date: datetime.date
    usd: int
    usd_foil: int
    euro: int
    euro_foil: int
    tix: int
