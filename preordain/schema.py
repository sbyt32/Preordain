from pydantic import BaseModel, Field
from preordain.enums import CardFormatLegalities, CardRarity
from preordain.models import CardFormats
from typing import Optional


class SchemaCardInfo(BaseModel):
    uri: str


class SchemaCardInfoTableInfo(SchemaCardInfo):
    name: str = Field(max_length=255)
    set: str = Field(max_length=12)
    id: str
    tcg_id: Optional[str]
    tcg_id_etch: Optional[str]
    groups: list[str]
    new_search: bool = Field(default=True)
    scrape_sales: bool = Field(default=False)


class SchemaCardInfoTableMetadata(SchemaCardInfo):
    rarity: CardRarity
    mana_cost: Optional[str]
    oracle_text: Optional[str]
    artist: Optional[str]


class SchemaCardInfoTableFormat(SchemaCardInfo, CardFormats):
    pass
