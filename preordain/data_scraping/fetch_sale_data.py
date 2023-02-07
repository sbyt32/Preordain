import time
import hashlib
import json
import logging
import psycopg
import datetime
import preordain.config_reader as cfg_reader
from scripts.update_config import update_config
from preordain.utils.connections import connect_db, send_response
from dateutil.parser import isoparse
log = logging.getLogger()

def _get_next_data(card_id:str, offset_value:int):
    url = f"https://mpapi.tcgplayer.com/v2/product/{card_id}/latestsales"
    # Check the notes for the structure of the Payload.
    payload = {
        "listingType":"All",
        "languages": [1], # We really only support about English at the moment, opt-in language support maybe later?
        "offset":offset_value,
        "limit":25
        }
    headers = {
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
        }

    return send_response("POST", url, json=payload, headers=headers)

def fetch_tcg_prices():
    # Define some stuff we will use later
    stop_future_looping = "UPDATE card_info.info SET new_search = false WHERE tcg_id = %s"

    start = time.perf_counter() # ? Used for timing the length to parse everything
    cfg = cfg_reader.read_config('UPDATES', 'database')

    conn, cur = connect_db()
    cur.execute("SELECT tcg_id, name, new_search FROM card_info.info'")
    res = cur.fetchall()

    for card_data in res:
        card_id:str = card_data[0]
        card_name:str = card_data[1]
        duplicate_merge:bool = card_data[2]
        offset_value = 0
        increment = 0

        resp = _get_next_data(card_id,offset_value)
        try:
            if resp['resultCount'] > 0:
                keep_adding_cards = True
        except TypeError:
            keep_adding_cards = False
        
        with conn.transaction() as tx1:
            while keep_adding_cards:
                log.debug(f"Getting {card_name} data with offset of {offset_value}, recieved {resp['resultCount']} results.")
                for sale_data in resp['data']:

                    order_id        = hashlib.sha256(card_id.encode('utf-8') + json.dumps(sale_data, sort_keys=True).encode('utf-8')).hexdigest()
                    order_date      = sale_data['orderDate']
                    condition:str       = sale_data['condition']
                    variant:str         = sale_data['variant']
                    qty:int             = sale_data['quantity']
                    buy_price:int      = sale_data['purchasePrice']
                    ship_price      = sale_data['shippingPrice']
                    try:
                        with conn.transaction() as tx2:
                            log.debug(f'Attempting to insert into table card_data_tcg with data | order date: {order_date}, cond: {condition}, variant: {variant}, qty: {qty}, sale $: {buy_price}, ship $: {ship_price}')
                            tx1.connection.execute("""
                            INSERT INTO card_data_tcg
                            VALUES (%s, %s,%s, %s,%s, %s,%s, %s)
                            """, (  order_id,
                                    card_id,
                                    order_date,
                                    condition,
                                    variant,
                                    qty,
                                    buy_price,
                                    ship_price,)
                                )
                    except psycopg.errors.UniqueViolation:
                        # * Three checks: 
                            # We should merge because of an override like adding a new card after initial fetch (new_search under card_info.info), 
                            # If there was no previous checks performed (cfg file check), 
                            # If the data point was added after the initial fetch (cfg file check against order date).
                        if duplicate_merge or cfg["tcg_sales"] == 'None' or isoparse(order_date) > isoparse(cfg["tcg_sales"]):
                            log.warning(f"Duplicate data for card {card_name}, approx. # {offset_value} - {offset_value + 25}, merging ID {order_id}")
                            tx1.connection.execute("""                            
                                UPDATE card_data_tcg
                                SET qty = card_data_tcg.qty + %s
                                WHERE order_id = %s

                            """,(qty, order_id)
                            )
                        else:
                            log.info(f"Grabbed {increment} new data points from {card_name}.")
                            keep_adding_cards = False
                            tx1.connection.execute(stop_future_looping, (card_id,))
                            break
                    else:
                        increment += 1
                    
                if resp['nextPage'] == "Yes": # ? Originally, it also contained  '...or keep_adding_cards == False:' Not sure if needed

                    offset_value += 25
                    resp = _get_next_data(card_id, offset_value)
                    time.sleep(.5)
                else:
                    tx1.connection.execute(stop_future_looping, (card_id,))
                    keep_adding_cards = False

    conn.close()
    # * After parsing, update the records to show the data.
    update_config('database', 'UPDATES', 'tcg_sales', str(datetime.datetime.now(datetime.timezone.utc)))
    log.debug(f"Elapsed time: {time.perf_counter() - start}") # ? Sends length to parse to debug
