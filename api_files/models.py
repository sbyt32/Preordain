from typing import TypeVar, Generic, Optional
import datetime
from enum import Enum
from pydantic import BaseModel, validator, Extra
from pydantic.generics import GenericModel
from enum import Enum
from typing import Any
# * Validator functions

# Check if value is a condition or not.  
def _verify_cond(condition: str):
    condition = condition.upper()
    if condition not in [cond for cond in CardConditions]:
        raise ValueError(f'Condition "{condition}" not a valid condition')
    return condition

def _verify_vari(variant: str):
    variant = variant.title()
    if variant not in [var for var in CardVariants]:
        raise ValueError(f'Variant "{variant}" is not a valid variant')
    return variant

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
    usd: float | None = None
    usd_foil: float | None = None
    euro: float | None = None
    euro_foil: float | None = None
    tix: float | None = None

# ? sales/...
class SaleData(BaseModel):
    order_date: datetime.datetime
    condition : CardConditions
    variant   : CardVariants
    quantity  : int
    buy_price : float
    ship_price: float

    _verify_condition = validator('condition', allow_reuse=True, pre=True)(_verify_cond)

# * Response Models
#   This is what you test against / import into FastAPI!

# ? card/...
    # ? card/search/...
class CardInformation(BaseModel):
    name: str
    set: str
    set_full: str
    id: str 
    last_updated: datetime.date
    prices: CardPrices

# ? sales/...
class RecentCardSales(BaseModel):
    card_name: str
    set_name: str
    tcg_id: str
    sale_data: list[SaleData]
    
# ? inventory/...
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
    _verify_condition = validator('condition', allow_reuse=True, pre=True, each_item=True)(_verify_cond)
    _verify_variant = validator('variant', allow_reuse=True, pre=True, each_item=True)(_verify_vari)


# * Generic Response & affiliates!

class RespStrings(str, Enum):
    # ! Error
    error_request:str = 'error_request'             # * For any Errors
    # * card/...
    card_info:str = 'card_info'                     # * /card/...
    # * sales/...
    daily_card_sales:str = 'daily_card_sales'       # * /daily/{set}/{col_num}
    recent_card_sales:str = 'recent_card_sales'     # * /card/{tcg_id}
    # * inventory/...
    retrieve_inventory:str = 'retrieve_inventory'   # * /inventory/...
    
ResponseDataTypes = TypeVar('ResponseDataTypes', list, dict)

class BaseResponse(GenericModel, Generic[ResponseDataTypes]):
    resp: RespStrings
    status: int
    info: Optional[dict]
    data: Optional[list[ResponseDataTypes]]

    @validator('info', pre=True)
    def check_for_info_or_data(cls, v, values):
        if v is None and values.get('data') is None:
            raise ValueError("must return either values and/or info")
        return v

    def dict(self,*args, **kwargs) -> dict[str, Any]:
        """
            Automaticaly exclude None values.
        """
        kwargs.pop("exclude_none", None)
        return super().dict(*args, exclude_none=True, **kwargs)
    
    class Config:
            title = 'Primary Response'
            # extra = Extra.forbid

