import logging
log = logging.getLogger()
from preordain.utils.connections import connect_db
from fastapi import APIRouter, Response, status
from preordain.information.utils import parse_data_for_response
from preordain.information.models import CardInformation
from preordain.models import BaseResponse
search_router = APIRouter()

@search_router.get('/{query}')
async def search_for_card(query: str, response: Response):
    conn, cur = connect_db()
    cur.execute("""
        SELECT
            DISTINCT ON (info.name, info.id) "name",
            info.set,
            sets.set_full,
            info.id,
            prices.date "last_updated",
            prices.usd,
            prices.usd_foil,
            prices.euro,
            prices.euro_foil,
            prices.tix
        FROM card_info.info AS "info"
        JOIN card_info.sets AS "sets"
            ON info.set = sets.set
        JOIN 
            (
                SELECT
                    prices.date,
                    prices.set,
                    prices.id,
                    prices.usd,
                    prices.usd_foil,
                    prices.euro,
                    prices.euro_foil,
                    prices.tix
                FROM 
                    card_data as "prices"
            ) AS "prices"
        ON prices.set = info.set
        AND prices.id = info.id
        WHERE LOWER(info.name) ILIKE %s
    """, ('%{}%'.format(query),))
    data = cur.fetchall()
    conn.close()
    if data:
        response.status_code = status.HTTP_200_OK
        return BaseResponse[CardInformation](data=parse_data_for_response(data), resp='search_query', status=response.status_code)
    response.status_code = status.HTTP_404_NOT_FOUND
    return BaseResponse(resp='no_results', status=response.status_code, info={'message': "No results found", 'query': query})
