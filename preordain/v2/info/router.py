from fastapi import APIRouter, Response, status
from preordain.v2.database import session
from preordain.v2.schema import (
    CardIndex,
    PriceTable,
    CardMetadataTable,
    SetTable,
    CardFormatTable,
)
from preordain.v2.info.models import CardData
from sqlalchemy.orm import aliased
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select

info_router = APIRouter()

price_cls = aliased(PriceTable, name="prices")
metadata_cls = aliased(CardMetadataTable, name="card_data")
legality_cls = aliased(CardFormatTable, name="legalities")

base_statement = (
    select(
        CardIndex.scryfall_uri,
        metadata_cls.card_name,
        metadata_cls.set_code,
        price_cls,
        metadata_cls,
        SetTable.set_name,
        legality_cls,
    )
    .join(CardIndex.prices)
    .where(CardIndex.scryfall_uri == price_cls.scryfall_uri)
    .join(CardIndex.card_metadata)
    .where(CardIndex.scryfall_uri == metadata_cls.scryfall_uri)
    .join(metadata_cls.set)
    .where(metadata_cls.set_code == SetTable.set_code)
    .join(CardIndex.legality)
    .where(CardIndex.scryfall_uri == legality_cls.scryfall_uri)
    # .order_by(metadata_cls.set_code)
    # .distinct(metadata_cls.set_code)
    .order_by(metadata_cls.card_name)
    .distinct(metadata_cls.card_name)
    .order_by(price_cls.date.desc())
)


@info_router.get("/search/{query}", response_model=list[CardData])
async def get_card_info(query: str):
    result = session.execute(
        base_statement.where(metadata_cls.card_name.icontains(query)).limit(10)
    )

    return jsonable_encoder(result.mappings().fetchall())


@info_router.get("/card/{uri}")
async def search_db_for_single_card(uri: str = "c9f8b8fb-1cd8-450e-a1fe-892e7a323479"):
    result = session.execute(base_statement.where(CardIndex.scryfall_uri.__eq__(uri)))
    return jsonable_encoder(result.mappings().fetchone())
