from fastapi import APIRouter, Response, status
from ..database import database_connection_v2
from ..schema import card_index, price_table

from sqlalchemy import select

info_router = APIRouter()


@info_router.get("/")
async def get_card_info():
    with database_connection_v2.connect() as conn:
        conn.execute(select(card_index).join(price_table))
