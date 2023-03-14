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


def process_sorting(currency: str, order: str):
    # Ugliest thing I've ever had to do.
    if currency.lower() == "usd":
        if order.lower() == "desc":
            query = """
                SELECT
                    card_info.info.name,
                    card_info.sets.set,
                    card_info.sets.set_full,
                    card_info.info.id,
                    date,
                    usd,
                    ROUND ( 100.0 * (change.usd_ct::numeric - change.usd_yesterday::numeric) / change.usd_yesterday::numeric, 2) || '%' AS usd_change
                FROM card_data
                JOIN card_info.info
                    ON card_data.set = card_info.info.set
                    AND card_data.id = card_info.info.id
                JOIN card_info.sets
                    ON card_data.set = card_info.sets.set
                JOIN
                    (
                        SELECT
                            date AS dt,
                            set,
                            id,
                            usd AS usd_ct,
                            lag(usd, 1) over (partition by set, id order by date(date)) AS usd_yesterday
                        FROM card_data
                        GROUP BY set, id, date, usd ORDER BY date DESC
                    ) AS change
                ON change.dt = card_data.date
                AND change.set = card_data.set
                AND change.id = card_data.id
                WHERE not usd IS NULL
                ORDER BY date DESC, ROUND( 100.0 * (change.usd_ct::numeric - change.usd_yesterday::numeric) / change.usd_yesterday::numeric, 2) DESC
                LIMIT 10
                """
        else:
            query = """
                SELECT
                    card_info.info.name,
                    card_info.sets.set,
                    card_info.sets.set_full,
                    card_info.info.id,
                    date,
                    usd,
                    ROUND ( 100.0 * (change.usd_ct::numeric - change.usd_yesterday::numeric) / change.usd_yesterday::numeric, 2) || '%' AS usd_change
                FROM card_data
                JOIN card_info.info
                    ON card_data.set = card_info.info.set
                    AND card_data.id = card_info.info.id
                JOIN card_info.sets
                    ON card_data.set = card_info.sets.set
                JOIN
                    (
                        SELECT
                            date AS dt,
                            set,
                            id,
                            usd AS usd_ct,
                            lag(usd, 1) over (partition by set, id order by date(date)) AS usd_yesterday
                        FROM card_data
                        GROUP BY set, id, date, usd ORDER BY date DESC
                    ) AS change
                ON change.dt = card_data.date
                AND change.set = card_data.set
                AND change.id = card_data.id
                WHERE not usd IS NULL
                ORDER BY date DESC, ROUND( 100.0 * (change.usd_ct::numeric - change.usd_yesterday::numeric) / change.usd_yesterday::numeric, 2) ASC
                LIMIT 10
                """
    else:
        if order.lower() == "desc":
            query = """
                SELECT
                    card_info.info.name,
                    card_info.sets.set,
                    card_info.sets.set_full,
                    card_info.info.id,
                    date,
                    euro,
                    ROUND ( 100.0 * (change.euro_ct::numeric - change.euro_yesterday::numeric) / change.euro_yesterday::numeric, 2) || '%' AS euro_change
                FROM card_data
                JOIN card_info.info
                    ON card_data.set = card_info.info.set
                    AND card_data.id = card_info.info.id
                JOIN card_info.sets
                    ON card_data.set = card_info.sets.set
                JOIN
                    (
                        SELECT
                            date AS dt,
                            set,
                            id,
                            euro AS euro_ct,
                            lag(euro, 1) over (partition by set, id order by date(date)) AS euro_yesterday
                        FROM card_data
                        GROUP BY set, id, date, euro ORDER BY date DESC
                    ) AS change
                ON change.dt = card_data.date
                AND change.set = card_data.set
                AND change.id = card_data.id
                WHERE not euro IS NULL
                ORDER BY date DESC, ROUND( 100.0 * (change.euro_ct::numeric - change.euro_yesterday::numeric) / change.euro_yesterday::numeric, 2) DESC
                LIMIT 10
                """
        else:
            query = """
                SELECT
                    card_info.info.name,
                    card_info.sets.set,
                    card_info.sets.set_full,
                    card_info.info.id,
                    date,
                    euro,
                    ROUND ( 100.0 * (change.euro_ct::numeric - change.euro_yesterday::numeric) / change.euro_yesterday::numeric, 2) || '%' AS euro_change
                FROM card_data
                JOIN card_info.info
                    ON card_data.set = card_info.info.set
                    AND card_data.id = card_info.info.id
                JOIN card_info.sets
                    ON card_data.set = card_info.sets.set
                JOIN
                    (
                        SELECT
                            date AS dt,
                            set,
                            id,
                            euro AS euro_ct,
                            lag(euro, 1) over (partition by set, id order by date(date)) AS euro_yesterday
                        FROM card_data
                        GROUP BY set, id, date, euro ORDER BY date DESC
                    ) AS change
                ON change.dt = card_data.date
                AND change.set = card_data.set
                AND change.id = card_data.id
                WHERE not euro IS NULL
                ORDER BY date DESC, ROUND( 100.0 * (change.euro_ct::numeric - change.euro_yesterday::numeric) / change.euro_yesterday::numeric, 2) ASC
                LIMIT 10
                """
    return query
