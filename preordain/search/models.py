import datetime
from pydantic import BaseModel
from preordain.models import CardPrices, BaseResponse
from pydantic import BaseModel
from preordain.search.exceptions import InvalidSearchQuery

resp_string: str = "search_query"  # * /search/{query}


class SearchQuery(BaseModel):
    def __init__(self, **data) -> None:
        super().__init__(**data)
        if len(self.query) >= 50:
            raise InvalidSearchQuery
        if len(self.query) <= 0:
            raise InvalidSearchQuery

    query: str


class CardInfoData(BaseModel):
    name: str
    set: str
    set_full: str
    id: str
    uri: str
    scrape_sales: bool
    last_updated: datetime.date
    prices: CardPrices


class SearchInformation(BaseResponse):
    resp = resp_string
    data: list[CardInfoData]

    class Config:
        schema_extra = {
            "example": {
                "resp": "search_query",
                "status": 200,
                "data": {
                    "name": "Ancient Grudge",
                    "set": "MM3",
                    "set_full": "Modern Masters 2017",
                    "id": "88",
                    "last_updated": "2023-02-05",
                    "prices": {
                        "usd": 12.34,
                        "usd_foil": 12.34,
                        "euro": 12.34,
                        "euro_foil": 12.34,
                        "tix": 12.34,
                    },
                },
            }
        }
        use_enum_values = True
