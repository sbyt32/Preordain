from functools import lru_cache
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
