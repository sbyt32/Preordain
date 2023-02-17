from pydantic import validator, BaseModel
from .exceptions import InvalidSearchQuery

class SearchQuery(BaseModel):
    query: str

    @validator('query')
    def sanititize_str(cls, v:str):
        if len(v) >= 50:
            raise InvalidSearchQuery
        if len(v) <= 0:
            raise InvalidSearchQuery
        return v

