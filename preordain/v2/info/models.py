from pydantic import BaseModel
import datetime


class PriceData(BaseModel):
    name: str
    set: str
    id: str
    date: datetime.date
    usd: float(2)
    usd_foil: float(2)
    euro: float(2)
    euro_foil: float(2)
    tix: float(2)
