import logging

log = logging.getLogger()
from preordain.utils.connections import connect_db
from fastapi import APIRouter, Response, status, Depends
from preordain.search.utils import parse_data_for_response
from preordain.search.models import SearchInformation
from preordain.search.models import SearchQuery
from preordain.models import BaseResponse
from preordain.exceptions import NotFound
search_router = APIRouter()

@search_router.get("/{query}")
# * https://github.com/tiangolo/fastapi/issues/1974
async def search_for_card(response: Response, query: SearchQuery = Depends()):
    conn, cur = connect_db()
    cur.execute(
        """
        SELECT 
            info.name,
            info.set,
            info.set_full,
            info.id,
            info.maxDate as "last_updated",
            price.usd,
            price.usd_foil,
            price.euro,
            price.euro_foil,
            price.tix
        FROM card_data price
        JOIN (
            SELECT 
                info.name, 
                info.set,
                sets.set_full,
                info.id,
                MAX(date) as maxDate
            FROM card_data
            JOIN card_info.info as info
                ON info.set = card_data.set
                AND info.id = card_data.id
            JOIN card_info.sets as sets
                ON sets.set = card_data.set
            GROUP BY info.set, info.id, info.name, sets.set_full
            ) info
        ON price.id = info.id AND price.set = info.set AND price.date = info.maxDate
        WHERE LOWER(info.name) ILIKE %s
    """,
        ("%{}%".format(query.query),),
    )
    data = cur.fetchall()
    conn.close()
    if data:
        response.status_code = status.HTTP_200_OK
        return SearchInformation(
            data=parse_data_for_response(data),
            status=response.status_code,
        )
    # response.status_code = 
    raise NotFound