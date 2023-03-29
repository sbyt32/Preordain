from preordain.models import BaseResponse, BaseCardData
from preordain.enums import CardConditions, CardVariants

# from pydantic import BaseModel
import datetime

RESP_STRING = "inventory_data"  # * /inventory/...


class InventoryData(BaseCardData):
    uri: str
    add_date: datetime.date
    quantity: int
    card_condition: CardConditions
    card_variant: CardVariants
    avg_cost: float
    change: str

    class Config:
        use_enum_values = True


class InventoryResponse(BaseResponse):
    resp = RESP_STRING
    data: list[InventoryData]

    class Config:
        schema_extra = {
            "example": {
                "resp": RESP_STRING,
                "status": 200,
                "data": [
                    {
                        "name": "Thalia, Guardian of Thraben",
                        "set": "vow",
                        "set_full": "Innistrad: Crimson Vow",
                        "id": "38",
                        "quantity": 2,
                        "card_condition": "NM",
                        "card_variant": "Normal",
                        "avg_cost": 2,
                        "change": "63.00",
                    }
                ],
            }
        }

        use_enum_values = True


class SuccessfulRequest(BaseResponse):
    resp = RESP_STRING
    info = {"message": "Modified Inventory"}
