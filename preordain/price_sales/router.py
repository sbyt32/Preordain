from fastapi import APIRouter, HTTPException, Response, status
from psycopg.errors import DatetimeFieldOverflow
from typing import Optional
from preordain.price_sales.utils import parse_data_for_response, check_card_exists
from preordain.utils.connections import connect_db
import logging
import re
log = logging.getLogger()


price_router = APIRouter(
    prefix="/price",
    tags=["Get Prices (from Scryfall)"]
)
sale_router = APIRouter(
    prefix="/sales",
    tags=["Get Sales (From TCGPlayer)"]
)

@price_router.get("/{date}",  description="Get the price data for the a certain day. YYYY-MM-DD format.")
async def get_single_day_data(date:str):
    if not re.match(r'^\d\d\d\d-(0?[1-9]|[1][0-2])-(0?[1-9]|[12][0-9]|3[01])', date):
        raise HTTPException(status_code=400, detail="Incorrect format.")
    else:
        conn, cur = connect_db()
        try:
            cur.execute("""

                SELECT 
                    card_info.info.name,
                    card_info.info.set,
                    card_info.sets.set_full,
                    card_info.info.id,
                    date
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

            """, (date,))
        except DatetimeFieldOverflow as e:
            # Placeholder, this is if the date isn't valid.
            return Exception("helpo")
        resp = cur.fetchall()
        conn.close()
        if resp:
            return parse_data_for_response(resp)
        else:
            raise HTTPException(status_code=404, detail=f"There is no price data for {date}")

@price_router.get("/{set}/{id}", description="Get the price data for one card. Last 25 results only.")
async def get_single_card_data(set: str, id: str, max: Optional[int] = 25):
    if max > 25:
        # TODO: Figure out how to know where the > 25 query came from.
        log.error("User attempted to search more than 25 queries, setting to 25.")
        max = 25

    conn, cur = connect_db()
    cur.execute(""" 
        
        SELECT 
            card_info.info.name,
            card_info.sets.set,
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
            card_data.set = %s AND card_data.id = %s
        ORDER BY date DESC
        LIMIT %s
        """,

        (set, id, max)
        )
    
    result = cur.fetchall()
    price_data_single_card = {}
    if result == []:
        raise HTTPException(status_code=404, detail="This card does not exist on the database!")
    else:
        price_data_single_card = {
                "name": result[0]['name'],
                "set": result[0]['set'],
                "set_full": result[0]['set_full'],
                "id": result[0]['id'],
                'data': []
            }
        # price_data_single_card["price_history"] = []
        for data in result:
            price_data_single_card['data'].append(
                {
                    "date": data['date'],
                    'prices': {
                        "usd" : data['usd'],
                        "usd_foil" : data['usd_foil'],
                        "euro" : data['euro'],
                        "euro_foil": data['euro_foil'],
                        "tix": data['tix'],
                    }
                }
            )
        log.debug(f"Returning card data for {price_data_single_card['name']}")
        return price_data_single_card

# Return the searched card + avg sale data. 
# * daily_card_sales
@sale_router.get("/recent/{set}/{col_num}", description="Get the most recent sales from this card. Max 25")
async def recent_card_sales_set_id(set:str, col_num:str, response: Response):
    searched_card = check_card_exists(set=set, col_num=col_num)
    if searched_card:
        conn, cur = connect_db()

        cur.execute("""
            SELECT 
                order_date,
                condition,
                variant,
                qty "quantity",
                buy_price,
                ship_price
            FROM 
                card_data_tcg
            JOIN card_info.info
                ON card_data_tcg.tcg_id = card_info.info.tcg_id
            JOIN card_info.sets
                ON card_info.info.set = card_info.sets.set
            WHERE 
                card_info.info.set = %s
                AND card_info.info.id = %s
            ORDER BY
                order_date desc
            LIMIT 25
        """, (set,col_num,))
        
        recieved_sale_data = cur.fetchall()
        searched_card['sale_data'] = recieved_sale_data

        response.status_code = status.HTTP_200_OK

        return {
            "resp": "recent_card_sale",
            "status": response.status_code,
            "data": {searched_card}
        }

@sale_router.get("/daily/{set}/{col_num}")
async def get_tcg_sales(set: str, col_num:str):
    searched_card = check_card_exists(set=set, col_num=col_num)
    if searched_card:
        conn, cur = connect_db()
        cur.execute("""
            SELECT 
                info.name,
                info.set,
                info.id,
                DATE_TRUNC('day', order_date) AS day, 
                COUNT("order_date") AS "number_of_sales",
                (SUM(buy_price * qty) / COUNT("order_date"))::numeric(10,2) as "avg_cost"
            FROM 
                card_data_tcg
            JOIN card_info.info AS info
                ON info.tcg_id = card_data_tcg.tcg_id
            WHERE info.set = %s
                AND info.id = %s
                AND condition = 'Near Mint'
                AND variant = 'Normal'
            GROUP BY 
                DATE_TRUNC('day', order_date), info.name, info.set,info.id
            ORDER BY 
                day ASC;
        """, (set,col_num,)
        )
        results = cur.fetchall()
        # return results
        conn.close()
        if results:
            resp = {
                "name": results[0]['name'],
                "set": results[0]['set'],
                "id": results[0]['id'],
                "data": []
            }
            for data in results:
                resp["data"].append(
                    {
                        "day": data["day"],
                        "sales": data["number_of_sales"],
                        "avg_cost": data["avg_cost"]
                    }
                )

            return resp