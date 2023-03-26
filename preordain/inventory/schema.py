from preordain.enums import CardConditions, CardVariants
from pydantic import BaseModel, Field
from typing import Optional
import datetime


# ? inventory/add | inventory/delete
class TableInventory(BaseModel):
    add_date: datetime.date
    uri: str
    qty: int = Field(ge=1)
    buy_price: float
    card_condition: CardConditions
    card_variant: CardVariants
