from pydantic import BaseModel, Field
from preordain.v1.enums import CardFormatLegalities, CardRarity
from preordain.v1.models import CardFormats
from typing import Optional


class SchemaCardInfo(BaseModel):
    uri: str


class SchemaCardInfoTableInfo(SchemaCardInfo):
    name: str = Field(max_length=255)
    set: str = Field(max_length=12)
    id: str
    tcg_id: Optional[str] = None
    tcg_id_etch: Optional[str] = None
    groups: list[str]
    new_search: bool = Field(default=True)
    scrape_sales: bool = Field(default=False)


class SchemaCardInfoTableMetadata(SchemaCardInfo):
    rarity: CardRarity
    mana_cost: Optional[str] = None
    oracle_text: Optional[str] = None
    artist: Optional[str] = None


class SchemaCardInfoTableFormat(SchemaCardInfo, CardFormats):
    pass