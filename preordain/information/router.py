import logging
log = logging.getLogger()
from preordain.utils.connections import connect_db, send_response
from fastapi import APIRouter, Response, status, Depends
from fastapi.exceptions import HTTPException
from preordain.information.utils import parse_data_for_response
from preordain.information.models import CardInformation
from preordain.models import BaseResponse
from preordain.dependencies import write_access


user_router = APIRouter(prefix="/card",tags=["Card Information, etc"])
search_router = APIRouter(prefix='/search', tags=["Search for a card"])
admin_router = APIRouter(prefix="/admin", tags=["Admin Panel"], dependencies=[Depends(write_access)])

# Return all cards
@user_router.get("/", 
    response_model=BaseResponse[CardInformation], 
    description="Return all cards that are being tracked.")
async def read_items(response: Response):
    conn, cur = connect_db()
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
    conn.close()
    if data:
        response.status_code = status.HTTP_200_OK
        return BaseResponse(resp='card_info', status=response.status_code, data=parse_data_for_response(data))
    response.status_code = status.HTTP_404_NOT_FOUND
    return BaseResponse(resp='error_request', status=response.status_code, info={'message': 'There are no cards in the database!'})

@user_router.get("/{set}/{col_num}",
    description="Look for a specific card based on the set and collector number",
    response_model=BaseResponse[CardInformation])
async def search_by_set_collector_num(set: str, col_num: str, response: Response):
    conn, cur = connect_db()
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

@user_router.get("/{group}",
    response_model=BaseResponse[CardInformation],
    description="Filter for cards by their groups.")
async def find_by_group(group: str, response: Response):
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


@search_router.get('/{query}')
async def search_for_card(query: str):
    conn, cur = connect_db()
    cur.execute("""
    SELECT * FROM card_info.info WHERE lower(card_info.info.name) ILIKE %s 

    """, ('%{}%'.format(query),))
    data = cur.fetchall()
    conn.close()
    if data:
        return data

@admin_router.post("/add/{set}/{coll_num}")
async def add_card_to_track(set: str, coll_num:str):

    resp = send_response('GET',f"https://api.scryfall.com/cards/search?q=set:{set}+cn:{coll_num}")

    try:
        if resp['object'] != "list":
            log.error("Not a card!")
            raise HTTPException(
                status_code=404, detail="This is not a card!"
            )

    except KeyError as e:
        # ? What does this look like, again?
        log.error(f"KeyError:{e}")

    else:
        if resp['total_cards'] != 1:
            error_msg = f"Recieved list with more than 1. Set:{set}, ID:{coll_num}"
            log.error(error_msg)
            return error_msg

        resp = resp['data'][0]
        conn, cur = connect_db()
        cur.execute("SELECT * from card_info.info where id = %s AND set= %s", (resp['collector_number'], resp['set']))
        if not cur.fetchall(): # * Run this section if no results (empty lists are False)                    
                if 'tcgplayer_etched_id' in resp:
                    tcg_etched_id = resp['tcgplayer_etched_id']
                else:
                    tcg_etched_id = None

                add_info_to_postgres = """
                    INSERT INTO card_info.info (name, set, id, uri, tcg_id, tcg_id_etch, new_search)

                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                    """
                # ? Uncomment below in production.
                cur.execute(add_info_to_postgres, (resp['name'], resp['set'], resp['collector_number'], resp['id'], resp['tcgplayer_id'], tcg_etched_id, True))
                conn.commit()

                log.info(f'Now tracking: {resp["name"]} from {resp["set_name"]}')
                return f'Now tracking: {resp["name"]} from {resp["set_name"]}'

        else:
            log.info(f'Already tracking: {resp["name"]} from {resp["set_name"]}')
            return f'Already tracking: {resp["name"]} from {resp["set_name"]}'

@admin_router.delete("/remove/{set}/{coll_num}")
async def remove_card_from_database(set:str, coll_num:str):

    conn, cur = connect_db()

    cur.execute("SELECT name, id, set from card_info.info where id = %s AND set = %s", (coll_num, set))

    fetched_card = cur.fetchone()
    if fetched_card:
        text_resp = f"Deleting: {fetched_card['name']} (Set: {fetched_card['set']}, Collector Num: {fetched_card['id']})"
        log.info(text_resp)
        cur.execute("DELETE FROM card_info.info WHERE id = %s AND set = %s", (coll_num,set))
        conn.commit()

    else:
        text_resp = f"Failed to delete, does not exist on DB (Set: {set}, Collector Num: {coll_num})"
        log.error(text_resp)

    return text_resp
