import logging
import datetime
import re
from .connections import connect_db, send_response
from .models import CardDataTable, SchemaCardInfoTableInfo


def _get_scryfall_bulk():
    bulk_data_link = send_response("GET", "https://api.scryfall.com/bulk-data")

    for bulk_data_info in bulk_data_link["data"]:
        if bulk_data_info["type"] == "default_cards":
            regex_pattern = re.compile(
                r"[0-9]{4}-[0-9]{2}-[0-9]{2}.*[0-9]{2}:[0-9]{2}:[0-9]{2}", re.IGNORECASE
            )
            fetch_time = regex_pattern.search(bulk_data_info["updated_at"])

            if fetch_time:
                file_name = fetch_time.group()

                file_name = file_name.replace("T", "_")
                file_name = file_name.replace(":", "")

                return send_response("GET", bulk_data_info["download_uri"]), file_name


def fetch_prices_from_scryfall() -> None:
    log = logging.getLogger()

    all_data, file_name = _get_scryfall_bulk()

    conn, cur = connect_db()

    card_data_query = """
        INSERT INTO card_data
        (uri, date, usd, usd_foil, usd_etch, euro, euro_foil, tix)

        VALUES (%(uri)s ,%(date)s,%(usd)s,%(usd_foil)s, %(usd_etch)s,%(euro)s,%(euro_foil)s,%(tix)s)
        """
    card_info_query = """
        INSERT INTO card_info.info (name, set, id, uri, tcg_id, tcg_id_etch, new_search)
        VALUES (%(name)s,%(set)s,%(id)s,%(uri)s,%(tcg_id)s,%(tcg_id_etch)s,%(new_search)s)

        ON CONFLICT DO NOTHING
        """
    for card in all_data:
        card_uri = card["id"]
        cur.execute(
            card_data_query,
            CardDataTable(
                uri=card_uri,
                date=datetime.datetime.strptime(file_name[0:10], "%Y-%m-%d").date(),
                usd=card["prices"]["usd"],
                usd_foil=card["prices"]["usd_foil"],
                usd_etch=card["prices"].get("usd_etch", None),
                euro=card["prices"]["eur"],
                euro_foil=card["prices"]["eur_foil"],
                tix=card["prices"]["tix"],
            ).dict(),
        )
        cur.execute(
            card_info_query,
            SchemaCardInfoTableInfo(
                name=card["name"],
                set=card["set"],
                id=card["collector_number"],
                uri=card_uri,
                tcg_id=card.get("tcgplayer_id", None),
                tcg_id_etch=card.get("tcgplayer_etched_id", None),
                groups=[],
                new_search=True,
                scrape_sales=False,
            ).dict(),
        )
    conn.commit()
    conn.close()
    log.debug(f"Parsed all {len(all_data)} cards")


if __name__ == "__main__":
    fetch_prices_from_scryfall()
