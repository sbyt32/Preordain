from preordain.models import BaseResponse
from preordain.enums import CardConditions, CardVariants
from pydantic import BaseModel

RESP_STRING = "retrieve_inventory"  # * /inventory/...


class InventoryData(BaseModel):
    name: str
    set: str
    quantity: int
    card_condition: CardConditions
    card_variant: CardVariants
    avg_cost: float

    class Config:
        use_enum_values = True


class InventoryResponse(BaseResponse):
    resp = RESP_STRING
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
