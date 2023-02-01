from fastapi import APIRouter, status, Response
from psycopg.rows import dict_row
from api_files.models import BaseResponse, InventoryData
import scripts.connect.to_database as to_db

router = APIRouter()
@router.get(
    path="/",
    description="Return your entire inventory.",
    response_model=BaseResponse[InventoryData])

# Return your entire inventory
# * retrieve_inventory
async def get_inventory(response: Response):
    conn, cur = to_db.connect_db(row_factory = dict_row)

    cur.execute("""
        SELECT
            info.name as name,
            set.set_full as set,
            SUM(inventory.qty) as quantity,
            inventory.card_condition as condition,
            inventory.card_variant as variant,
            (AVG(avg_price.total_qty) / SUM(inventory.qty))::numeric(10,2) as "avg_cost"
        FROM inventory as inventory
        JOIN card_info.info as info
            ON info.tcg_id = inventory.tcg_id
        JOIN card_info.sets as set
            ON info.set = set.set
        JOIN (
            SELECT 
                inventory.tcg_id,
                SUM (inventory.qty * inventory.buy_price)::numeric AS total_qty,
                inventory.card_condition,
                inventory.card_variant
            FROM inventory 
            GROUP BY
                inventory.tcg_id,
                inventory.card_condition,
                inventory.card_variant
        ) AS avg_price
            ON avg_price.tcg_id = inventory.tcg_id
            AND avg_price.card_condition = inventory.card_condition
            AND avg_price.card_variant = inventory.card_variant
        GROUP BY
            info.name,
            set.set_full,
            inventory.card_condition,
            inventory.card_variant
    """)
    data = cur.fetchall()
    response.status_code=status.HTTP_200_OK
    conn.close()
    return BaseResponse[InventoryData](data=data, status=response.status_code, resp='retrieve_inventory')