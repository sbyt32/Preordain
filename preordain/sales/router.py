from fastapi import APIRouter, HTTPException, Response, status
from preordain.utils.connections import connect_db
from preordain.sales.utils import check_card_exists, process_tcgp_data
from preordain.sales.models import SaleData, DailySales
from preordain.models import BaseResponse
import logging
import re

log = logging.getLogger()

sale_router = APIRouter()


# * daily_card_sales
@sale_router.get(
    "/recent/{set}/{col_num}",
    description="Get the most recent sales from this card. Max 25",
    responses={
        200: {
            "model": BaseResponse[SaleData],
            "description": "Retrieve your inventory.",
            "content": {
                "application/json": {
                    "example": {
                        "resp": "price_data",
                        "status": 200,
                        "data": [
                            {
                                "order_date": "2022-12-14T05:28:33.496000+00:00",
                                "condition": "NM",
                                "variant": "Normal",
                                "quantity": 1,
                                "buy_price": 0.81,
                                "ship_price": 0,
                            }
                        ],
                    }
                }
            },
        },
    },
)
async def recent_card_sales_set_id(set: str, col_num: str, response: Response):
    searched_card = check_card_exists(set=set, col_num=col_num)
    if searched_card:
        conn, cur = connect_db()

        cur.execute(
            """
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
                order_date DESC
            LIMIT 25
        """,
            (
                set,
                col_num,
            ),
        )

        data = cur.fetchall()
        if data:
            response.status_code = status.HTTP_200_OK
            return BaseResponse[SaleData](
                resp="recent_card_sales",
                status=response.status_code,
                data=process_tcgp_data(data),
            )
        response.status_code = status.HTTP_404_NOT_FOUND
        return BaseResponse(
            resp="no_results",
            status=response.status_code,
            info={"message": "No Results Found!"},
        )


@sale_router.get(
    "/daily/{set}/{col_num}", responses={200: {"model": BaseResponse[DailySales]}}
)
async def get_daily_sales_tcg(set: str, col_num: str, response: Response):
    searched_card = check_card_exists(set=set, col_num=col_num)
    if not searched_card:
        response.status_code = status.HTTP_404_NOT_FOUND
        return BaseResponse(
            resp="no_results",
            status=response.status_code,
            info={"message": "No Results Found!"},
        )
    conn, cur = connect_db()
    cur.execute(
        """
        SELECT 
            info.name,
            info.set,
            info.id,
            DATE_TRUNC('day', order_date) AS day, 
            COUNT("order_date") AS "number_of_sales",
            (SUM(buy_price * qty) / COUNT("order_date"))::numeric(10,2) as "avg_cost",
            CASE WHEN 
                LAG (
                    (SUM(buy_price * qty) / COUNT("order_date"))::numeric(10,2), 1) 
                    OVER 
                    (ORDER BY DATE_TRUNC('day',order_date)) 
                            is NULL THEN 0     
            ELSE 
                ROUND ( 
                    100.0 * 
                        (
                        (SUM(buy_price * qty) / COUNT("order_date"))::numeric(10,2) - LAG((SUM(buy_price * qty) / COUNT("order_date"))::numeric(10,2),1)
                        OVER 
                        (ORDER BY DATE_TRUNC('day',order_date))
                        )
                        / 
                        LAG((SUM(buy_price * qty) / COUNT("order_date"))::numeric(10,2),1) 
                        OVER 
                        (ORDER BY DATE_TRUNC('day',order_date)),2) 
            END || '%%' 
            AS daily_delta
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
            day DESC
        LIMIT 62
    """,
        (
            set,
            col_num,
        ),
    )
    results = cur.fetchall()
    conn.close()
    # TODO: Make this a function
    if results:
        resp = {
            "name": results[0]["name"],
            "set": results[0]["set"],
            "id": results[0]["id"],
            "sales": [],
        }
        for data in results:
            resp["sales"].append(
                {
                    "day": data["day"],
                    "sales": data["number_of_sales"],
                    "avg_cost": data["avg_cost"],
                    "day_change": data["daily_delta"],
                }
            )
        response.status_code = status.HTTP_200_OK
        return BaseResponse[DailySales](
            resp="daily_card_sales", status=response.status_code, data=[resp]
        )
