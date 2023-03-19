import logging

from preordain.utils.connections import connect_db
from fastapi import APIRouter, Response, status, Depends
from preordain.search.utils import parse_data_for_response
from preordain.search.models import SearchInformation
from preordain.search.models import SearchQuery
from preordain.exceptions import NotFound
from preordain.utils.get_last_update import get_last_update


log = logging.getLogger()
search_router = APIRouter()


@search_router.get("/{query}")
# * https://github.com/tiangolo/fastapi/issues/1974
async def search_for_card(
    response: Response,
    query: SearchQuery = Depends(),
    last_update: str = Depends(get_last_update),
):
    conn, cur = connect_db()
    cur.execute(
        """
        SELECT DISTINCT ON (info.name) name,
            info.name,
            info.id,
            info.set,
            sets.set_full,
            price.date as "last_updated",
            price.usd,
            price.usd_foil,
            price.usd_etch,
            price.euro,
            price.euro_foil,
            price.tix
        FROM card_data price
        JOIN card_info.info AS info
            ON price.uri = info.uri
        JOIN card_info.sets AS sets
            ON sets.set = info.set
        WHERE date = %s
        AND LOWER(info.name) ILIKE %s
    """,
        (
            last_update,
            "%{}%".format(query.query),
        ),
    )
    data = cur.fetchall()
    conn.close()
    if data:
        response.status_code = status.HTTP_200_OK
        return SearchInformation(
            data=parse_data_for_response(data),
            status=response.status_code,
        )
    response.status_code = status.HTTP_404_NOT_FOUND
    raise NotFound
