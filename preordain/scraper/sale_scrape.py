import hashlib
import json
import logging
import psycopg
import datetime
from preordain.logging_details import log_setup
from preordain import config
from preordain.scraper.models import CardDataTCGTable
from preordain.utils.connections import connect_db, send_response
from preordain.scraper.util import EnvVars
from dateutil.parser import isoparse
from typing import Union
from time import sleep


def fetch_sales_from_tcgplayer() -> None:
    log_setup()
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    stop_future_looping = (
        "UPDATE card_info.info SET new_search = false WHERE tcg_id = %s"
    )

    def get_next_data(card_tcg: str, offset: int) -> Union[dict, list, None]:
        url = f"https://mpapi.tcgplayer.com/v2/product/{card_tcg}/latestsales"
        payload = {
            "listingType": "All",
            "languages": [1],
            "offset": offset,
            "limit": 25,
        }
        headers = {
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        }

        return send_response("POST", url, json=payload, headers=headers)

    conn, cur = connect_db()
    cur.execute("SELECT tcg_id, name, new_search FROM card_info.info")

    for card_data in cur.fetchall():
        card_tcg: str = card_data["tcg_id"]
        card_name: str = card_data["name"]
        duplicate_merge: bool = card_data["new_search"]
        add_cards: bool = False
        offset: int = 0
        increment: int = 0

        tcg_json = get_next_data(card_tcg, offset)

        if tcg_json.get("resultCount", 0) > 0:
            add_cards = True
        else:
            add_cards = False

        with conn.transaction() as tx1:
            while add_cards:
                log.debug(
                    f"Getting {card_name} data with offset of {offset}, recieved {tcg_json['resultCount']} results."
                )
                for sale_data in tcg_json["data"]:
                    order_id = hashlib.sha256(
                        card_tcg.encode("utf-8")
                        + json.dumps(sale_data, sort_keys=True).encode("utf-8")
                    ).hexdigest()

                    data_insert = CardDataTCGTable(
                        order_id=order_id,
                        tcg_id=card_tcg,
                        order_date=sale_data["orderDate"],
                        condition=sale_data["condition"],
                        variant=sale_data["variant"],
                        qty=sale_data["quantity"],
                        buy_price=sale_data["purchasePrice"],
                        ship_price=sale_data["shippingPrice"],
                    ).dict()
                    try:
                        with conn.transaction() as tx2:
                            tx1.connection.execute(
                                """
                            INSERT INTO card_data_tcg
                            VALUES (
                                %(order_id)s, %(tcg_id)s,%(order_date)s, %(condition)s,
                                %(variant)s, %(qty)s,%(buy_price)s, %(ship_price)s)
                            """,
                                data_insert,
                            )
                    except psycopg.errors.UniqueViolation:
                        if (
                            duplicate_merge
                            or config.TCG_SALES == "None"
                            or isoparse(sale_data["orderDate"])
                            > isoparse(config.TCG_SALES)
                        ):
                            log.warning(
                                f"Duplicate data for card {card_name}, approx. # {offset} - {offset + 25}, merging ID {order_id}"
                            )
                            tx1.connection.execute(
                                """
                                UPDATE card_data_tcg
                                SET qty = card_data_tcg.qty + %s
                                where order_id = %s
                                """,
                                (sale_data["quantity"], order_id),
                            )
                        else:
                            log.info(
                                f"Grabbed {increment} new data points from {card_name}."
                            )
                            add_cards = False
                            tx1.connection.execute(stop_future_looping, (card_tcg,))
                            break
                    else:
                        increment += 1
                if tcg_json["nextPage"] == "Yes":
                    offset += 25
                    tcg_json = get_next_data(card_tcg, offset)
                    sleep(0.5)
                else:
                    tx1.connection.execute(stop_future_looping, (card_tcg,))
                    add_cards = False
    conn.commit()
    conn.close()
    EnvVars().update_env("TCG_SALES", str(datetime.datetime.now(datetime.timezone.utc)))


if __name__ == "__main__":
    fetch_sales_from_tcgplayer()
