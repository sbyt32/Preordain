from cachetools import cached, TTLCache

# from asyncache import cached
from fastapi import APIRouter, HTTPException, Response, status, Depends
from psycopg.errors import DatetimeFieldOverflow
from typing import Optional
from preordain.price.utils import (
    parse_data_single_card,
)
from preordain.utils.connections import connect_db
from preordain.utils.get_last_update import get_last_update
from preordain.price.models import (
    PriceDataMultiple,
    PriceDataSingle,
    PriceChange,
)
from preordain.utils.get_last_update import get_last_update, to_tomorrow
from preordain.utils.timer import timer
from preordain.price.enums import GrowthCurrency, GrowthDirections
from preordain.exceptions import NotFound
from datetime import datetime
from preordain.config import UPDATE_OFFSET
import logging

log = logging.getLogger()

price_router = APIRouter()


@cached(cache=TTLCache(maxsize=1024, ttl=to_tomorrow()))
@price_router.get(
    "/{set}/{id}",
    description="Get the price data for one card. Last 25 results only.",
    responses={
        200: {
            "model": PriceDataSingle,
            "description": "OK Request",
        },
    },
)
async def get_single_card_data(
    response: Response, set: str, id: str, max: Optional[int] = 31
):
    if abs(max) > 31:
        # TODO: Figure out how to know where the > 31 query came from.
        log.error("User attempted to search more than 31 queries, setting to 31.")
        max = 31

    conn, cur = connect_db()
    cur.execute(
        """
        SELECT
            card_info.info.name,
            card_info.sets.set,
            card_info.sets.set_full,
            card_info.info.id,
            date,
            usd,
            ROUND ( 100.0 *
                (usd::numeric - lag(usd, 1) over (partition by card_info.info.uri order by date(date))::numeric)
                /
                lag(usd, 1) over (partition by card_info.info.uri order by date(date))::numeric
            , 2) AS "usd_change",
            usd_foil,
            ROUND ( 100.0 *
                (usd_foil::numeric - lag(usd_foil, 1) over (partition by card_info.info.uri order by date(date))::numeric)
                /
                lag(usd_foil, 1) over (partition by card_info.info.uri order by date(date))::numeric
            , 2) AS "usd_foil_change",
            euro,
            ROUND ( 100.0 *
                (euro::numeric - lag(euro, 1) over (partition by card_info.info.uri order by date(date))::numeric)
                /
                lag(euro, 1) over (partition by card_info.info.uri order by date(date))::numeric
            , 2) AS "euro_change",
            euro_foil,
            ROUND ( 100.0 *
                (euro_foil::numeric - lag(euro_foil, 1) over (partition by card_info.info.uri order by date(date))::numeric)
                /
                lag(euro_foil, 1) over (partition by card_info.info.uri order by date(date))::numeric
            , 2) AS "euro_foil_change",
            tix,
            ROUND ( 100.0 *
                (tix::numeric - lag(tix, 1) over (partition by card_info.info.uri order by date(date))::numeric)
                /
                lag(tix, 1) over (partition by card_info.info.uri order by date(date))::numeric
            , 2) AS "tix_change"
        FROM card_data
        JOIN card_info.info
            ON card_data.uri = card_info.info.uri
        JOIN card_info.sets
            ON card_info.info.set = card_info.sets.set
        WHERE
            card_info.info.set = %s AND card_info.info.id = %s
        ORDER BY date DESC
        LIMIT %s
        """,
        (set, id, max),
    )

    data = cur.fetchall()

    if data:
        for value in data:
            for currency in ["usd", "usd_foil", "euro", "euro_foil", "tix"]:
                value[f"{currency}_change"] = f"{value[f'{currency}_change']}%"
        response.status_code = status.HTTP_200_OK
        return PriceDataSingle(
            status=response.status_code, data=parse_data_single_card(data)
        )
    response.status_code = status.HTTP_404_NOT_FOUND
    raise NotFound


# To Fix: Caching does not work on this endpoint but works on others?
# @cached(cache=TTLCache(maxsize=1024, ttl=round((datetime.today() + UPDATE_OFFSET - datetime.now()).total_seconds())))
@price_router.get("/changes/{growth}/{currency}")
async def get_biggest_gains(
    response: Response,
    currency: GrowthCurrency = str(GrowthCurrency.usd),
    growth: GrowthDirections = str(GrowthDirections.desc),
    last_update: str = Depends(get_last_update),
):
    # We can relax (I think) due to Pydantic's field validation. Execution is ~2000ms. Goal is < 500ms.
    conn, cur = connect_db()
    cur.execute(
        f"""
        SELECT
            card_info.info.name,
            card_info.sets.set,
            card_info.sets.set_full,
            card_info.info.id,
            date,
            {currency},
            ROUND ( 100.0 *
                ({currency}::numeric - lag({currency}, 1) over (partition by card_info.info.uri order by date(date))::numeric)
                /
                lag({currency}, 1) over (partition by card_info.info.uri order by date(date))::numeric
            , 2) AS "{currency}_change"
        FROM card_data
        JOIN card_info.info
            ON card_data.uri = card_info.info.uri
        JOIN card_info.sets
            ON card_info.info.set = card_info.sets.set
        WHERE NOT {currency} IS NULL
        AND {currency} >= '.50'
        AND date = '{last_update}'
        OR date = (SELECT lag(date, -1) over (order by date desc) from card_data GROUP BY date LIMIT 1)
        ORDER BY {currency}_change {growth} NULLS LAST
        LIMIT 10
        """
    )

    info = cur.fetchall()
    if info:
        for value in info:
            value[f"{currency}_change"] = f"{value[f'{currency}_change']}%"

        response.status_code = status.HTTP_200_OK
        return PriceChange(status=response.status_code, data=info)
    response.status_code = status.HTTP_404_NOT_FOUND
    return NotFound
