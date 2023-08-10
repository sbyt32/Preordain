from preordain.v2.models import PreordainData, CardPrices
from preordain.v2.enums import FormatLegalities
from pydantic import BaseModel, Field
import datetime


class CardMetadata(BaseModel):
    card_name: str
    set_code: str
    collector_number: str
    mana_cost: str | None
    oracle_text: str | None
    artist: str | None


class CardFormatLegalities(BaseModel):
    standard: FormatLegalities = Field(default=FormatLegalities.not_legal)
    historic: FormatLegalities = Field(default=FormatLegalities.not_legal)
    pioneer: FormatLegalities = Field(default=FormatLegalities.not_legal)
    modern: FormatLegalities = Field(default=FormatLegalities.not_legal)
    legacy: FormatLegalities = Field(default=FormatLegalities.not_legal)
    pauper: FormatLegalities = Field(default=FormatLegalities.not_legal)
    vintage: FormatLegalities = Field(default=FormatLegalities.not_legal)
    commander: FormatLegalities = Field(default=FormatLegalities.not_legal)


class CardData(PreordainData):
    scryfall_uri: str
    card_data: CardMetadata
    legalities: CardFormatLegalities
    prices: CardPrices
