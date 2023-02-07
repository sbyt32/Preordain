from preordain.models import CardConditions, CardVariants
from pydantic import BaseModel
from typing import Optional

class InventoryData(BaseModel):
    name: str
    set: str
    quantity: int
    condition: CardConditions
    variant: CardVariants
    avg_cost: float

    class Config:
        use_enum_values = True

# ? inventory/add | inventory/delete
class ModifyInventory(BaseModel):
    tcg_id      : Optional[str]
    set         : Optional[str]
    col_num     : Optional[str]
    qty         : int
    buy_price   : float
    condition   : CardConditions
    card_variant: CardVariants
