from pydantic import BaseModel
from typing import Optional


class CardInfoModel(BaseModel):
    name: str
    set: str
    id: str
    uri: str
    tcg_id: Optional[int]
    tcg_id_etch: Optional[int]
    new_search: bool = True
    groups: Optional[list[str]]
