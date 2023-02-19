from preordain.utils.connections import connect_db


def check_card_exists(tcg_id: str = None, set: str = None, col_num: str = None):
    if set and col_num or tcg_id:
        query = ""
        params = ()
        conn, cur = connect_db()

        if set and col_num:
            query = """
            SELECT name, set, id, tcg_id
            FROM card_info.info
            WHERE set = %s AND id = %s
            """
            params = (set, col_num)
        else:
            query = """
            SELECT name, set, id, tcg_id
            FROM card_info.info
            WHERE tcg_id = %s
            """
            params = (tcg_id,)
        cur.execute(query, params)
        identity = cur.fetchone()
        if identity:
            conn.close()
            return identity
    return False


def process_tcgp_data(data: list):
    conditions = [
        ("Near Mint", "NM"),
        ("Lightly Played", "LP"),
        ("Moderately Played", "MP"),
        ("Heavily Played", "HP"),
        ("Damaged", "DMG"),
    ]
    response = {
        "name": data[0]["name"],
        "set": data[0]["set"],
        "id": data[0]["id"],
    }
    response["data"] = []
    for card in data:
        for long, short in conditions:
            if card["condition"] == long:
                card["condition"] = short
                response["data"].append(
                    {
                        "order_date": card["order_date"],
                        "condition": card["condition"],
                        "variant": card["variant"],
                        "quantity": card["quantity"],
                        "buy_price": card["buy_price"],
                        "ship_price": card["ship_price"],
                    }
                )
                continue
    return response


def process_tcgp_data_single(data: list):
    response = {
        "name": data[0]["name"],
        "set": data[0]["set"],
        "id": data[0]["id"],
    }
    response["sales"] = []
    for cards in data:
        response["sales"].append(
            {
                "day": cards["day"],
                "sales": cards["number_of_sales"],
                "avg_cost": cards["avg_cost"],
                "day_change": cards["daily_delta"],
            }
        )
    return response
