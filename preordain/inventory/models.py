from preordain.models import CardConditions, CardVariants, BaseResponse, RespStrings
from pydantic import BaseModel
from typing import Optional
import datetime


class InventoryData(BaseModel):
    name: str
    set: str
    quantity: int
    card_condition: CardConditions
    card_variant: CardVariants
    avg_cost: float

    class Config:
        use_enum_values = True


# ? inventory/add | inventory/delete
class ModifyInventory(BaseModel):
    uri: str
    qty: int
    buy_price: float
    card_condition: CardConditions
    card_variant: CardVariants
    add_date: Optional[datetime.date]


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
