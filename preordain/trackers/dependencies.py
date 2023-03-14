from preordain.trackers.schema import CardInfoModel
from preordain.utils.connections import connect_db


async def duplicate_card(card: CardInfoModel):
    conn, cur = connect_db()

    query = """
        SELECT COUNT(*) FROM card_info.info WHERE set = %(set)s AND id = %(id)s
    """
    cur.execute(query, card.dict())

    count = cur.fetchone()
    if not count["count"] == 0:
        raise Exception("Hey write this later but duplicate!!")
    return card
