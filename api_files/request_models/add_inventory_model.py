from typing import Optional
from pydantic import BaseModel

class AddInventory(BaseModel):
    tcg_id      : Optional[str]
    set         : Optional[str]
    col_num     : Optional[str]
    qty         : int
    buy_price   : int
    condition   : str
    card_variant: str

