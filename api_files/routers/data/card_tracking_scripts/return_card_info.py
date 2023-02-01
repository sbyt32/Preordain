from fastapi import APIRouter, Response, status
from api_files.models import BaseResponse, CardInformation
# from api_files.response_class.pretty import PrettyJSONResp
from psycopg.rows import dict_row
import scripts.connect.to_database as to_db

from typing import Any, Sequence
from psycopg import Cursor

# Using Psycopg to create a row factory to parse the data correctly.
# https://www.psycopg.org/psycopg3/docs/advanced/rows.html#row-factory-create
class DictPriceFactory:
    def __init__(self, cursor: Cursor[Any]):
        self.fields = [c.name for c in cursor.description]
        self.dict_format = {'prices': {}}
        for c in cursor.description:
            if c.name in ['usd','usd_foil','euro','euro_foil','tix']:
                self.dict_format['prices'][c.name] =  self.dict_format.get(c.name, None)
            else:
                self.dict_format[c.name] = self.dict_format.get(c.name, c.name)
    
    def __call__(self, values: Sequence[Any]):
        card_info_data = dict(zip(self.fields[:5], values[:5]))
        card_info_prices = dict(zip(self.fields[5:], values[5:]))

        self.dict_format['prices'].update(card_info_prices)
        self.dict_format.update(card_info_data)
        return self.dict_format

router = APIRouter(
    prefix="/search",
)

# Return all cards
@router.get("/", 
    response_model=BaseResponse[CardInformation], 
    description="Return all cards that are being tracked.",)
async def read_items(response: Response):
    conn, cur = to_db.connect_db(row_factory = DictPriceFactory)
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
        return BaseResponse[CardInformation](data=data, resp='card_info', status=response.status_code).dict(exclude_none=True)
    response.status_code = status.HTTP_404_NOT_FOUND
    return BaseResponse(resp='error_request', status=response.status_code)

# Get a single card and return the data.
@router.get("/{set}/{col_num}",
    description="Look for a specific card based on the set and collector number",
    response_model=BaseResponse[CardInformation])
async def search_by_set_collector_num(set: str, col_num: str, response: Response):
    conn, cur = to_db.connect_db(row_factory = DictPriceFactory)
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
        return BaseResponse[CardInformation](data=data, resp='card_info', status=response.status_code).dict(exclude_none=True)
    response.status_code = status.HTTP_404_NOT_FOUND
    return BaseResponse(resp='error_request', status=response.status_code)

# Filter for cards by their grouping.
@router.get("/{group}",
    response_model=BaseResponse[CardInformation],
    description="Filter for cards by their groups.")
async def find_by_group(group: str, response: Response):
    conn, cur = to_db.connect_db(row_factory = DictPriceFactory)
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
    response.status_code = status.HTTP_200_OK
    conn.close()
    if data:
        response.status_code = status.HTTP_200_OK
        return BaseResponse[CardInformation](info={'group': group, 'info': 'ye'}, data=data, resp='card_info', status=response.status_code)
    response.status_code = status.HTTP_404_NOT_FOUND
    return BaseResponse(resp='error_request', status=response.status_code)