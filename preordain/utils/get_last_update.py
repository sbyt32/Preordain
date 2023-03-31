from cachetools import cached, TTLCache
from preordain.utils.connections import connect_db
from preordain.utils.timer import timer
from datetime import datetime
from preordain.config import UPDATE_OFFSET


def to_tomorrow():
    return round((datetime.today() + UPDATE_OFFSET - datetime.now()).total_seconds())


@cached(cache=TTLCache(maxsize=1024, ttl=to_tomorrow()))
def get_last_update():
    conn, cur = connect_db()
    cur.execute("SELECT MAX(date) as last_update from card_data limit 1")

    return cur.fetchone()["last_update"]
