from fastapi import APIRouter, Response, status
from api_files.models import BaseResponse, CardInformation
# from api_files.response_class.pretty import PrettyJSONResp
from psycopg.rows import dict_row
import scripts.connect.to_database as to_db


def parse_data_for_response(data: list):
    """
    Parse the data you recieved for this format.
    """
    card_data = []
    for cards in data:
        card_data.append(
            {
                'name': cards['name'],
                'set': cards['set'],
                'set_full': cards['set_full'],
                'id': cards['id'],
                'last_updated': cards['last_updated'],
                'prices': {
                    'usd': cards['usd'],
                    'usd_foil': cards['usd_foil'],
                    'euro': cards['euro'],
                    'euro_foil': cards['euro_foil'],
                    'tix': cards['tix'],
                }
            }
        )
    return card_data

router = APIRouter(
    prefix="/search",
)

# Return all cards
@router.get("/", 
    response_model=BaseResponse[CardInformation], 
    description="Return all cards that are being tracked.",)
async def read_items(response: Response):
    conn, cur = to_db.connect_db(row_factory = dict_row)
    cur.execute("""
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
        """
        )
    data = cur.fetchall()
    if data:
        response.status_code = status.HTTP_200_OK
        return BaseResponse(resp='card_info', status=response.status_code, data=parse_data_for_response(data))
    response.status_code = status.HTTP_404_NOT_FOUND
    return BaseResponse(resp='error_request', status=response.status_code, info={'message': 'There are no cards in the database!'})

# Get a single card and return the data.
@router.get("/{set}/{col_num}",
    description="Look for a specific card based on the set and collector number",
    response_model=BaseResponse[CardInformation])
async def search_by_set_collector_num(set: str, col_num: str, response: Response):
    conn, cur = to_db.connect_db(row_factory = dict_row)
    cur.execute(""" 
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
        WHERE   price.set = %s AND price.id = %s

        """,

        (set, col_num)
        )
    
    data = cur.fetchall()
    conn.close()
    if data:
        response.status_code = status.HTTP_200_OK
        return BaseResponse[CardInformation](resp='card_info', status=response.status_code,data=parse_data_for_response(data))
    response.status_code = status.HTTP_404_NOT_FOUND
    return BaseResponse(resp='error_request', status=response.status_code)

# # Filter for cards by their grouping.
@router.get("/{group}",
    response_model=BaseResponse[CardInformation],
    description="Filter for cards by their groups.")
async def find_by_group(group: str, response: Response):
    conn, cur = to_db.connect_db(row_factory = dict_row)
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
        WHERE %s = ANY (info.groups)
        ORDER BY 
            info.name, 
            info.id, 
            prices.date DESC

        """,
        (group,)
        )
    data = cur.fetchall()
    conn.close()
    if data:
        response.status_code = status.HTTP_200_OK
        return BaseResponse[CardInformation](info={'group': group, 'info': 'ye'}, data=parse_data_for_response(data), resp='card_info', status=response.status_code)
    response.status_code = status.HTTP_404_NOT_FOUND
    return BaseResponse(resp='error_request', status=response.status_code)