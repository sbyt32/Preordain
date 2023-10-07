from preordain.models import PreordainData, CardPrices
import datetime


class PriceData(PreordainData):
    date: datetime.date
    prices: CardPrices
