from preordain.utils.connections import connect_db


def get_card_from_set_id(set: str, id: str):
    conn, cur = connect_db()

    cur.execute(
        "SELECT uri FROM card_info.info where set = %s and id = %s",
        (
            set,
            id,
        ),
    )

    return cur.fetchone()["uri"]


# def get_set_id_from_uri(uri)


def validate_card_exists_from_uri(uri: str):
    conn, cur = connect_db()
    check = cur.execute(
        "SELECT EXISTS (SELECT 1 FROM card_info.info WHERE uri = %s)", (uri,)
    ).fetchone()["exists"]
    if check:
        return True
    return False


def validate_table_data():
    conn, cur = connect_db()
    return cur.execute(
        """
        SELECT
            EXISTS (SELECT 1 FROM card_info.info) AS info_exists,
            EXISTS (SELECT 1 from card_data) as price_exists
        """
    ).fetchone()
