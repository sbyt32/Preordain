from fastapi import APIRouter, Depends, Response, status
from preordain.utils.connections import connect_db, send_response
from preordain.inventory.models import ModifyInventory, InventoryResponse
from preordain.models import BaseResponse
from preordain.exceptions import NotFound
import arrow
import logging

log = logging.getLogger()

router = APIRouter()


@router.get(
    path="/",
    description="Return your entire inventory.",
    responses={
        200: {
            "model": InventoryResponse,
            "description": "Retrieve your inventory.",
        },
    },
)

# Return your entire inventory
async def get_inventory(response: Response):
    conn, cur = connect_db()

    cur.execute(
        """
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
    """
    )
    inventory = cur.fetchall()
    conn.close()
    if inventory:
        response.status_code = status.HTTP_200_OK
        return InventoryResponse(status=response.status_code, data=inventory).dict()
    raise NotFound



# ! Disabled for now
# @router.post("/add")
# async def add_to_inventory(inventory: ModifyInventory):
#     current_date = arrow.utcnow().date()
#     # ? If you have the set and collector number, but not the TCG_ID, it will pull that.
#     if inventory.set and inventory.col_num and not inventory.tcg_id:
#         resp = send_response("GET", f'https://api.scryfall.com/cards/{inventory.set.lower()}/{inventory.col_num.lower()}')
#         if inventory.card_variant == "Etched":
#             inventory.tcg_id = resp['tcgplayer_etched_id']
#         else:
#             inventory.tcg_id = str(resp['tcgplayer_id'])

#     if inventory.tcg_id:
#         conn, cur = connect_db()

#         cur.execute("""
#             SELECT
#                 EXISTS (
#                     SELECT 1
#                     FROM inventory
#                     WHERE tcg_id        = %s
#                     AND card_condition  = %s
#                     AND card_variant    = %s
#                     AND buy_price       = %s
#                     AND add_date        = %s
#                 )
#             """, (
#                     inventory.tcg_id,
#                     inventory.condition,
#                     inventory.card_variant,
#                     inventory.buy_price,
#                     current_date
#                 )
#         )

#         if cur.fetchone()['exists']:
#             cur.execute("""
#                 UPDATE inventory
#                 SET qty = inventory.qty + %s
#                 WHERE tcg_id = %s
#                 AND card_condition = %s
#                 AND card_variant = %s
#                 AND buy_price = %s
#                 AND add_date = %s
#                 """, (
#                     inventory.qty,
#                     inventory.tcg_id,
#                     inventory.condition,
#                     inventory.card_variant,
#                     inventory.buy_price,
#                     current_date
#                     )
#             )
#         else:
#             cur.execute("""
#                 INSERT INTO inventory
#                 VALUES (
#                     %s,
#                     %s,
#                     %s,
#                     %s,
#                     %s,
#                     %s
#                 )
#                 """, (
#                     current_date,
#                     inventory.tcg_id,
#                     inventory.qty,
#                     inventory.buy_price,
#                     inventory.condition,
#                     inventory.card_variant
#                     )
#             )

#         cur.execute("""
#             SELECT * FROM inventory
#             WHERE
#                 tcg_id = %s
#                 AND card_condition = %s
#                 AND card_variant = %s
#                 AND buy_price = %s
#                 AND add_date = %s
#             """, (
#                 inventory.tcg_id,
#                 inventory.condition,
#                 inventory.card_variant,
#                 inventory.buy_price,
#                 current_date
#                 )
#         )
#         inventory_check = cur.fetchone()
#         conn.commit()
#         return inventory_check


# @router.delete("/delete")
# async def remove_from_inventory():
#     pass
