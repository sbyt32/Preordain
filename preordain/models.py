from typing import TypeVar, Generic, Optional
import datetime
from enum import Enum
from pydantic import BaseModel, validator
from pydantic.generics import GenericModel
from enum import Enum
from typing import Any


# * Field Types

# ? All
class CardConditions(str, Enum):
    NM = 'NM'
    LP = 'LP'
    MP = 'MP'
    HP = 'HP'
    DMG = 'DMG'

class CardVariants(str, Enum):
    Normal = "Normal"
    Foil = "Foil"
    Etched = "Etched"

class CardPrices(BaseModel):
    usd: Optional[float] = 0.00
    usd_foil: Optional[float] = 0.00
    euro: Optional[float] = 0.00
    euro_foil: Optional[float] = 0.00
    tix: Optional[float] = 0.00

# ? sales/...
class SaleData(BaseModel):
    order_date: datetime.datetime
    condition : CardConditions
    variant   : CardVariants
    quantity  : int
    buy_price : float
    ship_price: float

# * Response Models
#   This is what you test against / import into FastAPI!

# ? card/...
    # ? card/search/...


# ? sales/...
class RecentCardSales(BaseModel):
    card_name: str
    set_name: str
    tcg_id: str
    sale_data: list[SaleData]
    
# ? inventory/...


# * Generic Response & affiliates!

class RespStrings(str, Enum):
    # ! Error
    error_request = 'error_request'             # * For any Errors
    no_results = 'no_results'                   # * For any Errors
    # * card/...
    card_info = 'card_info'                     # * /card/...
    # * search/{query}
    search_query = 'search_query'               # * /search/{query}
    # * sales/...
    daily_card_sales = 'daily_card_sales'       # * /daily/{set}/{col_num}
    recent_card_sales = 'recent_card_sales'     # * /card/{tcg_id}
    # * inventory/...
    retrieve_inventory = 'retrieve_inventory'   # * /inventory/...
    
ResponseDataTypes = TypeVar('ResponseDataTypes', list, dict)

class BaseResponse(GenericModel, Generic[ResponseDataTypes], BaseModel):
    resp: RespStrings
    status: int
    info: Optional[dict] = {}
    data: Optional[list[ResponseDataTypes]]

    @validator('info', pre=True)
    def check_for_info_or_data(cls, v, values):
        if v is None and values.get('data') is None:
            raise ValueError("must return either values and/or info")
        return v

    def dict(self,*args, **kwargs) -> dict[str, Any]:
        """
            Automaticaly exclude None values. Replaces regular model.dict()
        """
        kwargs.pop("exclude_defaults", None)
        return super().dict(*args, exclude_defaults=True, **kwargs)
    
    class Config:
            title = 'Primary Response'

