from preordain.enums import CardConditions, CardVariants
from pydantic import BaseModel, Field
from typing import Optional
import datetime


# ? inventory/add | inventory/delete
class TableInventory(BaseModel):
    uri: str
    qty: int = Field(ge=1)
    buy_price: float
    card_condition: CardConditions
    card_variant: CardVariants
    add_date: Optional[datetime.date]
