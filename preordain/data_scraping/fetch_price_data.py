from preordain.utils.connections import connect_db, send_response
from scripts.update_config import update_config
import arrow
import datetime
import logging
from time import sleep

log = logging.getLogger()


def query_price():
    conn, cur = connect_db()

    cur.execute("SELECT uri FROM card_info.info")
    records = cur.fetchall()

    log.debug(f"Parsing {len(records)} cards.")
    for uri in records:
        r = send_response("GET", f"https://api.scryfall.com/cards/{uri[0]}")
        sleep(0.2)
        insert_values = """
            INSERT INTO card_data (set, id, date, usd, usd_foil, euro, euro_foil, tix) 

            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)

            """
        cur.execute(
            insert_values,
            (
                r["set"],
                r["collector_number"],
                arrow.utcnow().format(
                    "YYYY-MM-DD"
                ),  # TODO: Convert this and exisiting data into ISO8601 w/ UTC TZ
                r["prices"]["usd"],
                r["prices"]["usd_foil"],
                r["prices"]["eur"],
                r["prices"]["eur_foil"],
                r["prices"]["tix"],
            ),
        )

    conn.commit()
    conn.close()
    log.debug(f"Parsed all {len(records)} cards")
    update_config(
        "database",
        "UPDATES",
        "price_fetch",
        str(datetime.datetime.now(datetime.timezone.utc)),
    )
