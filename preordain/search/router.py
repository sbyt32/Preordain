import logging

log = logging.getLogger()
from preordain.utils.connections import connect_db
from fastapi import APIRouter, Response, status
from preordain.information.utils import parse_data_for_response
from preordain.information.models import CardInformation
# from preordain.search.models import SearchQuery
from preordain.models import BaseResponse

search_router = APIRouter()

@search_router.get("/{query}")
async def search_for_card(query: str, response: Response):
    if len(query) >= 50:
        raise Exception("Hey maybe don't so much")
    if len(query) <= 0:
        raise Exception("Maybe like, search for a card")

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
        ("%{}%".format(query),),
    )
    data = cur.fetchall()
    conn.close()
    if data:
        response.status_code = status.HTTP_200_OK
        return BaseResponse[CardInformation](
            data=parse_data_for_response(data),
            resp="search_query",
            status=response.status_code,
        )
    response.status_code = status.HTTP_404_NOT_FOUND
    return BaseResponse(
        resp="no_results",
        status=response.status_code,
        info={"message": "No results found", "query": query},
    )
