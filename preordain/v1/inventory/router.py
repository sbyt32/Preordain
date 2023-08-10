from fastapi import APIRouter, Depends, Response, status
from preordain.utils.connections import connect_db, send_response
from preordain.v1.inventory.models import InventoryResponse, SuccessfulRequest
from preordain.v1.inventory.schema import TableInventory
from preordain.v1.models import BaseResponse
from preordain.v1.exceptions import NotFound
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
def get_inventory(response: Response):
    conn, cur = connect_db()

    cur.execute(
        """
        SELECT
            info.name as name,
            info.set,
            set.set_full as set_full,
            inventory.add_date,
            info.id,
            info.uri,
            SUM(inventory.qty) as quantity,
            inventory.card_condition as card_condition,
            inventory.card_variant as card_variant,
            (AVG(avg_price.total_qty) / SUM(inventory.qty))::numeric(10,2) as "avg_cost",
            CASE
                WHEN inventory.card_variant = 'Foil' THEN
                    ROUND (100.0 *
                    (
                        price.usd_foil::numeric - (AVG(avg_price.total_qty) / SUM(inventory.qty))::numeric
                    ) /
                    (
                        AVG(avg_price.total_qty) / SUM(inventory.qty))::numeric
                    , 2)
                WHEN inventory.card_variant = 'Etched' THEN
                    ROUND (100.0 * (price.usd_etch::numeric - (AVG(avg_price.total_qty) / SUM(inventory.qty))::numeric) / (AVG(avg_price.total_qty) / SUM(inventory.qty))::numeric, 2)
                ELSE
                    ROUND (100.0 * (price.usd::numeric - (AVG(avg_price.total_qty) / SUM(inventory.qty))::numeric) / (AVG(avg_price.total_qty) / SUM(inventory.qty))::numeric, 2)
            END AS "change"
        FROM inventory as inventory
        JOIN card_info.info as info
            ON info.uri = inventory.uri
        JOIN card_info.sets as set
            ON info.set = set.set
        JOIN (
            SELECT
                inventory.uri,
                SUM (inventory.qty * inventory.buy_price)::numeric AS total_qty,
                inventory.card_condition,
                inventory.card_variant
            FROM inventory
            GROUP BY
                inventory.uri,
                inventory.card_condition,
                inventory.card_variant
        ) AS avg_price
            ON avg_price.uri = inventory.uri
            AND avg_price.card_condition = inventory.card_condition
            AND avg_price.card_variant = inventory.card_variant
        JOIN (
            SELECT
                price.uri,
                price.usd,
                PRICE.usd_foil,
                price.usd_etch
            FROM card_data AS price
            WHERE price.date = (SELECT MAX(date) as last_update from card_data)
        ) AS price
            ON price.uri = inventory.uri
        GROUP BY
            info.name,
            info.set,
            set.set_full,
            inventory.add_date,
            info.id,
            info.uri,
            price.usd,
            price.usd_foil,
            price.usd_etch,
            inventory.card_condition,
            inventory.card_variant
    """
    )
    inventory = cur.fetchall()
    conn.close()
    if inventory:
        response.status_code = status.HTTP_200_OK
        return InventoryResponse(status=response.status_code, data=inventory)
    raise NotFound


@router.post(
    "/add/",
    description="Add cards to the inventory.",
    responses={
        201: {
            "model": SuccessfulRequest,
            "description": "Successfully Added to Inventory.",
        }
    },
)
async def add_to_inventory(inventory: TableInventory, response: Response):
    # Could we do this with a single "CASE WHERE..." statement?
    # Decide if update or add new
    conn, cur = connect_db()
    cur.execute(
        """
        SELECT
            EXISTS (
                SELECT 1
                FROM inventory
                WHERE add_date      = %(add_date)s
                AND uri             = %(uri)s
                AND card_condition  = %(card_condition)s
                AND card_variant    = %(card_variant)s
                AND buy_price       = %(buy_price)s
            )
        """,
        inventory.dict(),
    )

    if cur.fetchone()["exists"]:
        cur.execute(
            """
            UPDATE inventory
            SET qty = inventory.qty + %(qty)s
            WHERE uri = %(uri)s
            AND card_condition   = %(card_condition)s
            AND card_variant = %(card_variant)s
            AND buy_price = %(buy_price)s
            AND add_date = %(add_date)s
            """,
            inventory.dict(),
        )
    else:
        cur.execute(
            """
            INSERT INTO inventory
            VALUES (
                %(add_date)s,
                %(uri)s,
                %(qty)s,
                %(buy_price)s,
                %(card_condition)s,
                %(card_variant)s
            )
            """,
            inventory.dict(),
        )

    conn.commit()
    cur.execute(
        """
        SELECT
            EXISTS (
                SELECT 1
                FROM inventory
                WHERE uri           = %(uri)s
                AND card_condition  = %(card_condition)s
                AND card_variant    = %(card_variant)s
                AND buy_price       = %(buy_price)s
                AND add_date        = %(add_date)s
            )
        """,
        inventory.dict(),
    )

    if cur.fetchone()["exists"]:
        response.status_code = status.HTTP_201_CREATED
        return SuccessfulRequest(status=response.status_code)


# Is Delete the correct? Probably.
@router.post("/delete/", status_code=204)
async def remove_from_inventory(inventory: TableInventory):
    conn, cur = connect_db()
    cur.execute(
        """
        SELECT
            EXISTS (
                SELECT 1
                FROM inventory
                WHERE uri           = %(uri)s
                AND card_condition  = %(card_condition)s
                AND qty             = %(qty)s
                AND card_variant    = %(card_variant)s
                AND add_date        = %(add_date)s
            )
        """,
        inventory.dict(),
    )
    print(inventory.dict())
    if cur.fetchone()["exists"]:
        print(inventory.dict())
        cur.execute(
            """
            DELETE FROM inventory
                WHERE uri           = %(uri)s
                AND card_condition  = %(card_condition)s
                AND qty             = %(qty)s
                AND card_variant    = %(card_variant)s
                AND add_date        = %(add_date)s
        """,
            inventory.dict(),
        )
        conn.commit()
    return


@router.delete("/clear/", status_code=status.HTTP_204_NO_CONTENT)
async def clear_inventory():
    conn, cur = connect_db()
    cur.execute("DELETE FROM inventory")
    conn.commit()
    return
