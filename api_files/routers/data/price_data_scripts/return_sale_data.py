import scripts.connect.to_database as to_db
from fastapi import APIRouter, Response, status
from api_files.models import RecentCardSales
from psycopg.rows import dict_row


def _check_card_exists(tcg_id:str = None, set:str = None, col_num:str = None):
    if set and col_num or tcg_id:
        query = ""
        params = ()
        conn, cur = to_db.connect_db(row_factory = dict_row)

        if set and col_num:
            query = """
            SELECT name, set, id, tcg_id
            FROM card_info.info
            WHERE set = %s AND id = %s
            """
            params = (set, col_num)
        else:
            query = """
            SELECT name, set, id, tcg_id
            FROM card_info.info
            WHERE tcg_id = %s 
            """
            params = (tcg_id,)
        cur.execute(query,params)
        identity = cur.fetchone()
        if identity:
            conn.close()
            return identity
    return False

router = APIRouter(
    prefix="/sales",
)

@router.get("/", status_code=400)
async def root_access():
    return {
        "resp": "error",
        "status": 501,
        "message": "To be implemented later.",
    }

# Get the most recent sales from this card. Updates every week
# * recent_card_sales
@router.get("/card/{tcg_id}", description="Get the most recent sales from this card. Updates every week")
async def recent_card_sales_tcg_id(tcg_id:str, response: Response):
    searched_card = _check_card_exists(tcg_id=tcg_id)
    if searched_card:
        cur = to_db.connect_db(row_factory = dict_row)[1]

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
            "resp": "recent_card_sale",
            "status": response.status_code,
            "data": {searched_card}
        }

# Return the searched card + last sale data. 
# * daily_card_sales
@router.get("/daily/{set}/{col_num}")
async def get_tcg_sales(set: str, col_num:str):
    searched_card = _check_card_exists(set=set, col_num=col_num)
    if searched_card:
        conn, cur = to_db.connect_db(row_factory = dict_row)
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