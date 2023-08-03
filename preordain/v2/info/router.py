from fastapi import APIRouter, Response, status
from preordain.v2.database import database_connection_v2, session
from preordain.v2.schema import CardIndex, PriceTable
from preordain.v2.info.models import PriceData
from sqlalchemy.orm import aliased
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select

info_router = APIRouter()

price_cls = aliased(PriceTable, name="prices")


# , response_model=list[PriceData]
@info_router.get("/", response_model=list[PriceData])
async def get_card_info():
    result = session.execute(
        select(CardIndex.scryfall_uri, price_cls)
        .join(CardIndex.prices)
        .where(CardIndex.scryfall_uri == price_cls.scryfall_uri)
        .limit(10)
    )
    return jsonable_encoder(result.mappings().fetchall())
