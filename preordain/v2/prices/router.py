from fastapi import APIRouter
from preordain.v2.database import session
from preordain.v2.schema import CardIndex, PriceTable, CardMetadataTable
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import aliased

price_router = APIRouter()

price_cls = aliased(PriceTable, name="prices")
metadata_cls = aliased(CardMetadataTable, name="card_data")


@price_router.get("/price/{set_code}/{collector_number}")
async def get_card_prices(set_code: str, collector_number: str):
    result = session.execute(
        select(price_cls, metadata_cls)
        .where(metadata_cls.set_code == set_code)
        .where(metadata_cls.collector_number == collector_number)
        .join(CardIndex.prices)
        .where(CardIndex.scryfall_uri == price_cls.scryfall_uri)
        .join(CardIndex.card_metadata)
        .where(CardIndex.scryfall_uri == metadata_cls.scryfall_uri)
        .limit(31)
    )

    return jsonable_encoder(result.mappings().fetchall())
