# This is just not enabled rn

from fastapi import APIRouter, Response, status
from preordain.utils.connections import connect_db, send_response
from preordain.internal.util import get_scryfall_bulk
from preordain.schema import SchemaCardInfoTableInfo

# from functools import lru_cache

admin_route = APIRouter()


@admin_route.post("/sets/", status_code=status.HTTP_204_NO_CONTENT)
async def update_set_info():
    conn, cur = connect_db()

    for sets in send_response("GET", "https://api.scryfall.com/sets")["data"]:
        cur.execute(
            """
            INSERT INTO card_info.sets (set, set_full, release_date)
            VALUES (%s, %s, %s)

            ON CONFLICT DO NOTHING
            """,
            (sets["code"], sets["name"], sets["released_at"]),
        )
    conn.commit()
    print("Hello, Sets are updated!")


@admin_route.post("/info/")
async def update_card_info():
    conn, cur = connect_db()

    query = """
        INSERT INTO card_info.info (name, set, id, uri, tcg_id, tcg_id_etch, new_search)
        VALUES (%(name)s,%(set)s,%(id)s,%(uri)s,%(tcg_id)s,%(tcg_id_etch)s,%(new_search)s)

        ON CONFLICT DO NOTHING
    """

    cards = get_scryfall_bulk()[0]

    if (
        len(cards)
        == cur.execute("SELECT COUNT(*) FROM CARD_INFO.INFO").fetchone()["count"]
    ):
        return

    for card in cards:
        cur.execute(
            query,
            SchemaCardInfoTableInfo(
                name=card["name"],
                set=card["set"],
                id=card["collector_number"],
                uri=card["id"],
                tcg_id=card.get("tcgplayer_id", None),
                tcg_id_etch=card.get("tcgplayer_etched_id", None),
                groups=[],
                new_search=True,
                scrape_sales=False,
            ),
        )
    conn.commit()
