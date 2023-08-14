import datetime
from pydantic import ConfigDict, BaseModel
from typing import Optional, Union
from preordain.v1.models import BaseResponse
from preordain.v1.enums import CardConditions, CardVariants

daily_sales_str: str = "daily_card_sales"  # * /daily/{set}/{col_num}
recent_sales_str: str = "recent_card_sales"  # * /card/{tcg_id}


class RecentSaleData(BaseModel):
    order_date: datetime.datetime
    condition: CardConditions
    variant: CardVariants
    quantity: int
    buy_price: float
    ship_price: float
    model_config = ConfigDict(
        use_enum_values=True,
        json_schema_extra={
            "example": {
                "resp": "price_data",
                "status": 200,
                "data": [
                    {
                        "order_date": "2022-12-14T05:28:33.496000+00:00",
                        "condition": "NM",
                        "variant": "Normal",
                        "quantity": 1,
                        "buy_price": 0.81,
                        "ship_price": 0,
                    }
                ],
            }
        },
    )


class DailySaleData(BaseModel):
    day: datetime.date
    sales: int
    avg_cost: float
    day_change: Optional[str] = None
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "resp": "daily_card_sales",
                "status": 200,
                "data": {
                    "name": "Ancient Grudge",
                    "set": "MM3",
                    "id": "88",
                    "sales": [
                        {
                            "day": "2022-12-14T00:00:00+00:00",
                            "sales": 7,
                            "avg_cost": 17.2,
                            "day_change": "12.34%",
                        }
                    ],
                },
            }
        }
    )


class DailySales(BaseModel):
    name: str
    set: str
    id: str
    sales: list[Union[DailySaleData, RecentSaleData]]
    model_config = ConfigDict(extra="forbid")


class CardSaleResponse(BaseResponse):
    resp: str
    data: DailySales
