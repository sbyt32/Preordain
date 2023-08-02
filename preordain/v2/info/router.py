from fastapi import APIRouter, Response, status
from preordain.v2.database import database_connection_v2
from preordain.v2.schema import card_index, price_table
from preordain.v2.info.models import PriceData

from sqlalchemy import select

info_router = APIRouter()


@info_router.get("/", response_model=list[PriceData])
async def get_card_info():
    with database_connection_v2.connect() as conn:
        result = conn.execute(
            select(
                card_index,
                price_table.c.date,
                price_table.c.usd,
                price_table.c.usd_foil,
                price_table.c.euro,
                price_table.c.euro_foil,
                price_table.c.tix,
            )
            .join(price_table, card_index.c.scryfall_uri == price_table.c.scryfall_uri)
            .limit(1)
        )
    return result.mappings().all()
