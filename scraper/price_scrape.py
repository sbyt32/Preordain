import logging
from time import sleep
import arrow

from .connections import connect_db, send_response
from .models import CardDataTable

# python -m preordain.scraper.price_scrape


def fetch_prices_from_scryfall() -> None:
    log = logging.getLogger()
    conn, cur = connect_db()

    cur.execute("SELECT uri FROM card_info.info")
    records: list[dict[str, str]] = cur.fetchall()

    log.debug(f"Parsing {len(records)}")
    for cards in records:
        card: dict = send_response(
            "GET", f"https://api.scryfall.com/cards/{cards['uri']}"
        )
        sleep(0.2)
        query = """
            INSERT INTO card_data
            (set, id, date, usd, usd_foil, euro, euro_foil, tix)

            VALUES (%(set)s,%(id)s,%(date)s,%(usd)s,%(usd_foil)s,%(euro)s,%(euro_foil)s,%(tix)s)

            """
        params = CardDataTable(
            set=card["set"],
            id=card["collector_number"],
            date=arrow.utcnow().format("YYYY-MM-DD"),
            usd=card["prices"]["usd"],
            usd_foil=card["prices"]["usd_foil"],
            euro=card["prices"]["eur"],
            euro_foil=card["prices"]["eur_foil"],
            tix=card["prices"]["tix"],
        ).dict()
        cur.execute(query, params)
    conn.commit()
    conn.close()
    log.debug(f"Parsed all {len(records)} cards")


if __name__ == "__main__":
    fetch_prices_from_scryfall()
