from pydantic import BaseModel
from typing import Optional


class CardInfoModel(BaseModel):
    uri: str
