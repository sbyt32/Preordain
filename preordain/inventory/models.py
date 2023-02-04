from preordain.models import CardConditions, CardVariants
# from preordain.utils.validators import verify_cond, verify_vari
from pydantic import BaseModel, validator
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
    # Verify
    # _verify_condition = validator('condition', allow_reuse=True, pre=True, each_item=True)(verify_cond)
    # _verify_variant = validator('variant', allow_reuse=True, pre=True, each_item=True)(verify_vari)

# ? inventory/add | inventory/delete
class ModifyInventory(BaseModel):
    tcg_id      : Optional[str]
    set         : Optional[str]
    col_num     : Optional[str]
    qty         : int
    buy_price   : float
    condition   : CardConditions
    card_variant: CardVariants

    # _verify_condition = validator('condition', allow_reuse=True, pre=True, each_item=True)(verify_cond)
    # _verify_variant = validator('variant', allow_reuse=True, pre=True, each_item=True)(verify_vari)
