from fastapi import APIRouter, HTTPException, Response, status
from api_files.response_models.card_info import CardInfo
from api_files.response_class.pretty import PrettyJSONResp
from psycopg.rows import dict_row
import scripts.connect.to_database as to_db

router = APIRouter(
    prefix="/search"
)

# Return all cards
@router.get(
    path="/", 
    status_code=200, 
    response_class=PrettyJSONResp, 
    response_model=CardInfo, 
    description="Return all cards that are being tracked.")
async def read_items(response: Response):
    conn, cur = to_db.connect_db(row_factory = dict_row)
    cur.execute("""
        SELECT 
            info.name,
            info.set,
            info.set_full,
            info.id,
            info.maxDate as "date",
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
    resp = cur.fetchall()
    # return resp
    if resp:
        response.status_code = status.HTTP_200_OK
        card_data = []
        for cards in resp:
            card_data.append(
                {
                    'name': cards['name'],
                    'set': cards['set'],
                    'set_full': cards['set_full'],
                    'id': cards['id'],
                    'last_update': cards['date'],
                    'usd': cards['usd'],
                    'usd_foil': cards['usd_foil'],
                    'euro': cards['euro'],
                    'euro_foil': cards['euro_foil'],
                    'tix': cards['tix'],
                }
            )

        return {
            "resp"      : "card_data",
            "status"    : response.status_code,
            "data"      : card_data
        }
    else:
        return {}
# Filter for cards by their grouping.
@router.get("/{group}")
async def find_by_group(group: str):
    conn, cur = to_db.connect_db(row_factory = dict_row)
    cur.execute(""" 
        
        SELECT   
            DISTINCT ON (info.name, info.id) "name",
            sets.set_full AS "set",
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
    resp = cur.fetchall()
    if resp == []:
        return "No Groups Found!"
        # return [{}]
    else:
        return resp

# Get a single card card and return the data for that card.
@router.get("/{set}/{col_num}",
    description="Look for a specific card based on that cards set + collector number"
    )
async def search_by_set_collector_num(set: str, col_num: str, response: Response):
    conn, cur = to_db.connect_db(row_factory = dict_row)
    cur.execute(""" 
        SELECT 
            info.name,
            info.set_full,
            info.id,
            info.maxDate as "date",
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
    
    single_card = cur.fetchone()
    if single_card:
        response.status_code = status.HTTP_200_OK
        return {
            "resp"      : "card_data",
            "status"    : response.status_code,
            "data"      : {
                    'name': single_card['name'],
                    'set_full': single_card['set_full'],
                    'id': single_card['id'],
                    'last_update': single_card['date'],
                    'prices': {
                        'usd': single_card['usd'],
                        'usd_foil': single_card['usd_foil'],
                        'euro': single_card['euro'],
                        'euro_foil': single_card['euro_foil'],
                        'tix': single_card['tix'],
                    }
            }
        }
    else:
        raise HTTPException(status_code=404, detail="This card does not exist on the database!")