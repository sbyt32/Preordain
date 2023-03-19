from functools import lru_cache
from preordain.utils.connections import connect_db

# This won't update past the first update. Fix it.
@lru_cache
def get_last_update():
    conn, cur = connect_db()
    cur.execute("SELECT MAX(date) as last_update from card_data")

    return cur.fetchone()["last_update"]