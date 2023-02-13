import datetime
from pydantic import BaseModel
from typing import Optional
from preordain.models import CardConditions, CardVariants


class SaleData(BaseModel):
    order_date: datetime.datetime
    condition: CardConditions
    variant: CardVariants
    quantity: int
    buy_price: float
    ship_price: float

    class Config:
        use_enum_values = True


class RecentCardSales(BaseModel):
    card_name: str
    set_name: str
    tcg_id: str
    sale_data: list[SaleData]


class DailySaleData(BaseModel):
    day: datetime.date
    sales: int
    avg_cost: float
    day_change: Optional[str]


class DailySales(BaseModel):
    name: str
    set: str
    id: str
    sales: list[DailySaleData]
