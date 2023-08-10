from fastapi import APIRouter, Response, status
from preordain.v2.database import session
from preordain.v2.schema import CardIndex, PriceTable, CardMetadataTable, SetTable
from preordain.v2.info.models import CardData
from sqlalchemy.orm import aliased
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select

info_router = APIRouter()

price_cls = aliased(PriceTable, name="prices")
metadata_cls = aliased(CardMetadataTable, name="card_data")

base_statement = (
    select(CardIndex.scryfall_uri, price_cls, metadata_cls, SetTable.set_name)
    .join(CardIndex.prices)
    .where(CardIndex.scryfall_uri == price_cls.scryfall_uri)
    .join(CardIndex.card_metadata)
    .where(CardIndex.scryfall_uri == metadata_cls.scryfall_uri)
    .join(metadata_cls.set)
    .where(metadata_cls.set_code == SetTable.set_code)
    .distinct(metadata_cls.set_code)
)


# , response_model=list[CardData]
@info_router.get("/search/{query}")
async def get_card_info(query: str):
    result = session.execute(
        base_statement.where(metadata_cls.card_name.icontains(query)).limit(10)
    )
    return jsonable_encoder(result.mappings().fetchall())
