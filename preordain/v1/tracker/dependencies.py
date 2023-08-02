from preordain.tracker.schema import CardInfoModel
from preordain.utils.connections import connect_db


# If there was a duplicate card on card_info.info, this would have triggered, no longer need it.

# async def duplicate_card(card: CardInfoModel):
#     conn, cur = connect_db()

#     query = """
#         SELECT COUNT(*) FROM card_info.info WHERE set = %(set)s AND id = %(id)s
#     """
#     cur.execute(query, card.dict())

#     count = cur.fetchone()
#     if not count["count"] == 0:
#         raise Exception("Hey write this later but duplicate!!")
#     return card
