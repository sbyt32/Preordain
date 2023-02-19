from preordain.models import CardConditions, CardVariants, BaseResponse, RespStrings
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
    tcg_id: Optional[str]
    set: Optional[str]
    col_num: Optional[str]
    qty: int
    buy_price: float
    condition: CardConditions
    card_variant: CardVariants


class InventoryResponse(BaseResponse):
    resp = RespStrings.retrieve_inventory
    data: dict[str, str] = InventoryData

    class Config:
        schema_extra = {
            "example": {
                "resp": "retrieve_inventory",
                "status": 200,
                "data": [
                    {
                        "name": "Thalia, Guardian of Thraben",
                        "set": "Innistrad: Crimson Vow",
                        "quantity": 2,
                        "condition": "NM",
                        "variant": "Normal",
                        "avg_cost": 2,
                    }
                ],
            }
        }
        use_enum_values = True
