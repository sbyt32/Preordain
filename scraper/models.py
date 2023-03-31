from pydantic import BaseModel, Field
from typing import Optional
import datetime


class CardDataTable(BaseModel):
    uri: str
    date: datetime.date
    usd: Optional[str]
    usd_foil: Optional[str]
    usd_etch: Optional[str]
    euro: Optional[str]
    euro_foil: Optional[str]
    tix: Optional[str]


class CardDataTCGTable(BaseModel):
    order_id: str
    tcg_id: str
    order_date: datetime.datetime
    condition: str
    variant: str
    qty: int
    buy_price: int
    ship_price: int


class SchemaCardInfoTableInfo(BaseModel):
    name: str = Field(max_length=255)
    set: str = Field(max_length=12)
    id: str
    uri: str
    tcg_id: Optional[int]
    tcg_id_etch: Optional[int]
    groups: Optional[list[str]]
    new_search: bool = Field(default=True)
    scrape_sales: bool = Field(default=False)
