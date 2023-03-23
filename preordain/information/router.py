from preordain.utils.connections import connect_db
from fastapi import APIRouter, Response, status
from preordain.information.utils import parse_data_for_response
from preordain.information.models import CardInformation, CardPurchaseLink
from preordain.exceptions import NotFound
from preordain.utils.find_missing import get_card_from_set_id

user_router = APIRouter()


@user_router.get(
    "/{set}/{col_num}",
    description="Look for a specific card based on the set and collector number",
)
async def search_by_set_collector_num(set: str, col_num: str, response: Response):
    conn, cur = connect_db()
    uri = get_card_from_set_id(set, col_num)
    cur.execute(
        """
            SELECT
                info.name,
                info.set,
                sets.set_full,
                info.id,
                price.date,
                price.usd,
                price.usd_foil,
                price.usd_etch,
                price.euro,
                price.euro_foil,
                price.tix
            FROM card_info.info AS info
            JOIN card_info.sets AS sets
                ON sets.set = info.set
            JOIN (
                SELECT
                    price.uri,
                    price.usd,
                    price.usd_foil,
                    price.usd_etch,
                    price.euro,
                    price.euro_foil,
                    price.tix,
                    price.date
                FROM card_data as price
                WHERE price.uri = %s
                ORDER BY date DESC
                LIMIT 1
                ) AS price
            ON price.uri = info.uri
            WHERE info.uri = %s

        """,
        (uri, uri),
    )

    data = cur.fetchall()
    conn.close()
    if data:
        response.status_code = status.HTTP_200_OK
        return CardInformation(
            status=response.status_code, data=parse_data_for_response(data)
        )
    raise NotFound


@user_router.get("/{group}", description="Filter for cards by their groups.")
async def find_by_group(group: str, response: Response):
    conn, cur = connect_db()
    cur.execute(
        """

        SELECT
            DISTINCT ON (info.name, info.id, info.set) "name",
            info.set,
            sets.set_full,
            info.id,
            prices.date AS "date",
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
                    prices.uri,
                    prices.usd,
                    prices.usd_foil,
                    prices.euro,
                    prices.euro_foil,
                    prices.tix
                FROM
                    card_data as "prices"
                WHERE prices.date = (SELECT MAX(date) as last_update from card_data)
            ) AS "prices"
        ON prices.uri = info.uri
        WHERE %s = ANY (info.groups)
        ORDER BY
            info.name,
            info.id,
            info.set,
            prices.date DESC

        """,
        (group,),
    )
    data = cur.fetchall()
    cur.execute(
        """
        SELECT
            groups.group_name,
            groups.description,
            (SELECT COUNT(*) AS QTY FROM card_info.info WHERE %s = ANY(groups))
        FROM card_info.groups AS groups
        WHERE %s = groups.group_name
    """,
        (
            group,
            group,
        ),
    )
    info = cur.fetchone()
    conn.close()
    if data:
        response.status_code = status.HTTP_200_OK
        return CardInformation(
            info=info, status=response.status_code, data=parse_data_for_response(data)
        )

    raise NotFound


@user_router.get("/buylinks/{set}/{col_num}")
async def get_purchase_links(set: str, col_num: str, response: Response):
    # Update later
    conn, cur = connect_db()
    resp = cur.execute(
        "SELECT tcg_id FROM card_info.info WHERE set = %s AND id = %s",
        (
            set,
            col_num,
        ),
    )
    if resp:
        response.status_code = status.HTTP_200_OK
        return CardPurchaseLink(status=response.status_code, data=resp.fetchone())
    pass
