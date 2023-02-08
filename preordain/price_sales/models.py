import datetime
from pydantic import BaseModel
from preordain.models import CardConditions, CardVariants

class SaleData(BaseModel):
    order_date: datetime.datetime
    condition : CardConditions
    variant   : CardVariants
    quantity  : int
    buy_price : float
    ship_price: float

class RecentCardSales(BaseModel):
    card_name: str
    set_name: str
    tcg_id: str
    sale_data: list[SaleData]