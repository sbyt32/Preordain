import scripts.connect.to_database as to_db
from fastapi import APIRouter, Response, status
from typing import Union
from psycopg.rows import dict_row
# from api_files.exceptions import RootException

router = APIRouter(
    prefix="/sales",
)

def _check_card_exists(tcg_id:str = None, set:str = None, col_num:str = None):

    if set and col_num or tcg_id:
        query = ""
        params = ()
        cur = to_db.connect_db()[1]

        if set and col_num:
            query = """
            SELECT COUNT(*)
            FROM card_info.info
            WHERE set = %s AND id = %s
            """
            params = (set, col_num)
        else:
            query = """
            SELECT COUNT(*)
            FROM card_info.info
            WHERE tcg_id = %s 
            """
            params = (tcg_id,)
        cur.execute(query,params)
        
        if cur.fetchone():
            return True
    return False


@router.get("/", status_code=400)
async def root_access():
    return {
        "resp": "error",
        "status": 501,
        "message": "To be implemented later.",
    }

@router.get("/card/{tcg_id}", description="Get the most recent sales from this card. Updates every week")
async def get_tcg_sales(tcg_id:str, response: Response):
    cur = to_db.connect_db(row_factory = dict_row)[1]

    cur.execute("""
        SELECT
            info.name "card_name",
            sets.set_full "set_name",
            info.tcg_id 
        FROM card_info.info AS info
        JOIN card_info.sets AS sets
            ON info.set = sets.set
        WHERE
            info.tcg_id = %s
    """, (tcg_id,))

    searched_card = cur.fetchone()

    if searched_card:

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
                card_data_tcg.tcg_id = %s
            ORDER BY
                order_date desc
            LIMIT 25
        """, (tcg_id,))
        
        recieved_sale_data = cur.fetchall()


        searched_card['sale_data'] = recieved_sale_data
        response.status_code = status.HTTP_200_OK

        return {
            "resp": "hello",
            "status": response.status_code,
            "data": [searched_card]
        }

@router.get("/card/{set}/{col_num}")
async def get_tcg_sales(set: str, col_num:str):
    if _check_card_exists(set=set, col_num=col_num):
        cur = to_db.connect_db(row_factory = dict_row)[1]

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