from preordain.utils.connections import connect_db


def parse_data_for_response(data: list):
    """
    Parse the data you recieved for this format.
    """
    card_data = []
    for cards in data:
        card_data.append(
            {
                "name": cards["name"],
                "set": cards["set"],
                "set_full": cards["set_full"],
                "id": cards["id"],
                "date": cards["date"],
                "prices": {
                    "usd": cards["usd"],
                    "usd_foil": cards["usd_foil"],
                    "euro": cards["euro"],
                    "euro_foil": cards["euro_foil"],
                    "tix": cards["tix"],
                },
            }
        )
    return card_data


def parse_data_single_card(data: list):
    """
    Parse the data you recieved for this format.
    """
    card_data = {
        "name": data[0]["name"],
        "set": data[0]["set"],
        "set_full": data[0]["set_full"],
        "id": data[0]["id"],
        "prices": [],
    }

    for cards in data:
        card_data["prices"].append(
            {
                "date": cards["date"],
                "usd": cards["usd"],
                "usd_change": cards["usd_change"],
                "usd_foil": cards["usd_foil"],
                "usd_foil_change": cards["usd_foil_change"],
                "euro": cards["euro"],
                "euro_change": cards["euro_change"],
                "euro_foil": cards["euro_foil"],
                "euro_foil_change": cards["euro_foil_change"],
                "tix": cards["tix"],
                "tix_change": cards["tix_change"],
            }
        )

    return card_data


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
    for card in data:
        for long, short in conditions:
            if card["condition"] == long:
                card["condition"] = short
                continue
    return data
