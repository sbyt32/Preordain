import logging
from time import sleep
import arrow
import re
from .connections import connect_db, send_response
from .models import CardDataTable


def fetch_prices_from_scryfall() -> None:
    log = logging.getLogger()

    bulk_data_link = send_response("https://api.scryfall.com/bulk-data")

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

                all_data = send_response(bulk_data_info["download_uri"])

                conn, cur = connect_db()

                sleep(0.2)
                query = """
                    INSERT INTO card_data
                    (uri, date, usd, usd_foil, usd_etch, euro, euro_foil, tix)

                    VALUES (%(uri)s ,%(date)s,%(usd)s,%(usd_foil)s, %(usd_etch)s,%(euro)s,%(euro_foil)s,%(tix)s)
                    """
                for card in all_data:
                    params = CardDataTable(
                        uri=card["id"],
                        date=arrow.utcnow().format("YYYY-MM-DD"),
                        usd=card["prices"]["usd"],
                        usd_foil=card["prices"]["usd_foil"],
                        usd_etch=card["prices"]["usd_etch"],
                        euro=card["prices"]["eur"],
                        euro_foil=card["prices"]["eur_foil"],
                        tix=card["prices"]["tix"],
                    ).dict()
                    cur.execute(query, params)
                conn.commit()
                conn.close()
                log.debug(f"Parsed all {len(all_data)} cards")


if __name__ == "__main__":
    fetch_prices_from_scryfall()
