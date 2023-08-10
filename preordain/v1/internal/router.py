# This is just not enabled rn

from fastapi import APIRouter, status
from preordain.utils.connections import connect_db, send_response
from preordain.v1.internal.util import get_scryfall_bulk
from preordain.v1.schema import (
    SchemaCardInfoTableInfo,
    SchemaCardInfoTableFormat,
    SchemaCardInfoTableMetadata,
)

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

    card_info_query = """
        INSERT INTO card_info.info (name, set, id, uri, tcg_id, tcg_id_etch, new_search)
        VALUES (%(name)s,%(set)s,%(id)s,%(uri)s,%(tcg_id)s,%(tcg_id_etch)s,%(new_search)s)

        ON CONFLICT DO NOTHING
    """
    card_format_query = """
        INSERT INTO card_info.formats
            (uri, standard, historic, pioneer, modern, legacy, pauper, vintage, commander)
        VALUES
            (%(uri)s,%(standard)s,%(historic)s,%(pioneer)s,%(modern)s,%(legacy)s,%(pauper)s,%(vintage)s,%(commander)s)
        ON CONFLICT DO NOTHING
    """

    card_metadata_query = """
        INSERT INTO card_info.metadata
            (uri, rarity, mana_cost, oracle_text, artist)
        VALUES
            (%(uri)s,%(rarity)s, %(mana_cost)s,%(oracle_text)s,%(artist)s)
        ON CONFLICT DO NOTHING
    """

    cards = get_scryfall_bulk()[0]

    # No new updates. This isn't a great way to check tbh.
    if (
        len(cards)
        == cur.execute("SELECT COUNT(*) FROM CARD_INFO.INFO").fetchone()["count"]
    ):
        return

    for card in cards:
        uri = card["id"]
        cur.execute(
            """
            INSERT INTO card_info.info
                (name, set, id, uri, tcg_id, tcg_id_etch, new_search)
            VALUES
                (%(name)s,%(set)s,%(id)s,%(uri)s,%(tcg_id)s,%(tcg_id_etch)s,%(new_search)s)
            ON CONFLICT DO NOTHING
            """,
            SchemaCardInfoTableInfo(
                name=card["name"],
                set=card["set"],
                id=card["collector_number"],
                uri=uri,
                tcg_id=card.get("tcgplayer_id", None),
                tcg_id_etch=card.get("tcgplayer_etched_id", None),
                groups=[],
                new_search=True,
                scrape_sales=False,
            ).dict(),
        )
        cur.execute(
            """
            INSERT INTO card_info.formats
                (uri, standard, historic, pioneer, modern, legacy, pauper, vintage, commander)
            VALUES
                (%(uri)s,%(standard)s,%(historic)s,%(pioneer)s,%(modern)s,%(legacy)s,%(pauper)s,%(vintage)s,%(commander)s)
            ON CONFLICT DO NOTHING
            """,
            SchemaCardInfoTableFormat(
                uri=uri,
                standard=card["legalities"]["standard"],
                historic=card["legalities"]["historic"],
                pioneer=card["legalities"]["pioneer"],
                modern=card["legalities"]["modern"],
                legacy=card["legalities"]["legacy"],
                pauper=card["legalities"]["pauper"],
                vintage=card["legalities"]["vintage"],
                commander=card["legalities"]["commander"],
            ).dict(),
        )
        cur.execute(
            """
            INSERT INTO card_info.metadata
                (uri, rarity, mana_cost, oracle_text, artist)
            VALUES
                (%(uri)s,%(rarity)s, %(mana_cost)s,%(oracle_text)s,%(artist)s)
            ON CONFLICT DO NOTHING
            """,
            SchemaCardInfoTableMetadata(
                uri=uri,
                rarity=card["rarity"],
                mana_cost=card.get("mana_cost", None),
                oracle_text=card.get("oracle_text", None),
                artist=card.get("artist", None),
            ).dict(),
        )
    conn.commit()
