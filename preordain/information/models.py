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