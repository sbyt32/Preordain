from fastapi import APIRouter, HTTPException, Response, status
from psycopg.errors import DatetimeFieldOverflow
from typing import Optional
from preordain.price.utils import parse_data_for_response, parse_data_single_card
from preordain.utils.connections import connect_db
from preordain.price.models import PriceDataMultiple, PriceDataSingle
from preordain.exceptions import NotFound
import logging
import re

log = logging.getLogger()

price_router = APIRouter()


@price_router.get(
    "/{date}",
    description="Get the price data for the a certain day. YYYY-MM-DD format.",
    responses={
        200: {
            "model": PriceDataMultiple,
            "description": "OK Request",
        },
    },
)
async def get_single_day_data(date: str, response: Response):
    if not re.match(r"^\d\d\d\d-(0?[1-9]|[1][0-2])-(0?[1-9]|[12][0-9]|3[01])", date):
        raise HTTPException(status_code=400, detail="Incorrect format.")
    conn, cur = connect_db()
    try:
        cur.execute(
            """

            SELECT
                card_info.info.name,
                card_info.info.set,
                card_info.sets.set_full,
                card_info.info.id,
                date,
                usd,
                usd_foil,
                euro,
                euro_foil,
                tix
            FROM card_data
            JOIN card_info.info
                ON card_data.set = card_info.info.set
                AND card_data.id = card_info.info.id
            JOIN card_info.sets
                ON card_data.set = card_info.sets.set
            WHERE
                date = %s

        """,
            (date,),
        )
    except DatetimeFieldOverflow as e:
        # Placeholder, this is if the date isn't valid.
        return Exception("helpo")
    data = cur.fetchall()
    conn.close()
    if data:
        response.status_code = status.HTTP_200_OK
        return PriceDataMultiple(
            status=response.status_code, data=parse_data_for_response(data)
        )
    response.status_code = status.HTTP_404_NOT_FOUND
    raise NotFound


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
    response: Response, set: str, id: str, max: Optional[int] = 25
):
    if abs(max) > 25:
        # TODO: Figure out how to know where the > 25 query came from.
        log.error("User attempted to search more than 25 queries, setting to 25.")
        max = 25

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
            ROUND ( 100.0 * (change.usd_ct::numeric - change.usd_yesterday::numeric) / change.usd_yesterday::numeric, 2) || '%%' AS usd_change,
            usd_foil,
            ROUND ( 100.0 * (change.usd_foil_ct::numeric - change.usd_foil_yesterday::numeric) / change.usd_foil_yesterday::numeric, 2) || '%%' AS usd_foil_change,
            euro,
            ROUND ( 100.0 * (change.euro_ct::numeric - change.euro_yesterday::numeric) / change.euro_yesterday::numeric, 2) || '%%' AS euro_change,
            euro_foil,
            ROUND ( 100.0 * (change.euro_foil_ct::numeric - change.euro_foil_yesterday::numeric) / change.euro_foil_yesterday::numeric, 2) || '%%' AS euro_foil_change,
            tix,
            ROUND ( 100.0 * (change.tix_ct::numeric - change.tix_yesterday::numeric) / change.tix_yesterday::numeric, 2) || '%%' AS tix_change
        FROM card_data
        JOIN card_info.info
            ON card_data.set = card_info.info.set
            AND card_data.id = card_info.info.id
        JOIN card_info.sets
            ON card_data.set = card_info.sets.set
        JOIN
            (
                SELECT
                    date AS dt,
                    usd AS usd_ct,
                    lag(usd, 1) over (order by date(date)) AS usd_yesterday,
                    usd_foil AS usd_foil_ct,
                    lag(usd_foil, 1) over (order by date(date)) AS usd_foil_yesterday,
                    euro AS euro_ct,
                    lag(euro, 1) over (order by date(date)) AS euro_yesterday,
                    euro_foil AS euro_foil_ct,
                    lag(euro_foil, 1) over (order by date(date)) AS euro_foil_yesterday,
                    tix AS tix_ct,
                    lag(tix, 1) over (order by date(date)) AS tix_yesterday
                FROM card_data
                WHERE
                card_data.set = %s AND card_data.id = %s
                GROUP BY date, usd, usd_foil, euro, euro_foil, tix ORDER BY date DESC
            ) AS change
        ON change.dt = card_data.date
        WHERE
            card_data.set = %s AND card_data.id = %s
        ORDER BY date DESC
        LIMIT %s
        """,
        (set, id, set, id, max),
    )

    data = cur.fetchall()

    if data:
        response.status_code = status.HTTP_200_OK
        return PriceDataSingle(
            status=response.status_code, data=parse_data_single_card(data)
        )
    response.status_code = status.HTTP_404_NOT_FOUND
    raise NotFound
