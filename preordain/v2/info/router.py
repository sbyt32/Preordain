from fastapi import APIRouter, Response, status
from preordain.v2.database import database_connection_v2, session
from preordain.v2.schema import CardIndex, PriceTable
from preordain.v2.info.models import PriceData
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select

info_router = APIRouter()


# , response_model=list[PriceData]
@info_router.get("/")
async def get_card_info():
    result = session.scalars(
        select(PriceTable.usd, CardIndex.scryfall_uri)
        .join(CardIndex, CardIndex.scryfall_uri == PriceTable.scryfall_uri)
        .limit(10)
    )
    return jsonable_encoder(result.all())

    # with database_connection_v2.connect() as conn:
    #     result = conn.execute(
    #         select(
    #             card_index,
    #             price_table.c.date,
    #             price_table.c.usd,
    #             price_table.c.usd_foil,
    #             price_table.c.euro,
    #             price_table.c.euro_foil,
    #             price_table.c.tix,
    #         )
    #         .join(price_table, card_index.c.scryfall_uri == price_table.c.scryfall_uri)
    #         .limit(1)
    #     )
    # return result.mappings().all()
