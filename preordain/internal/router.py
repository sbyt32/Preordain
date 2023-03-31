# This is just not enabled rn

from fastapi import APIRouter, Response, status
from preordain.utils.connections import connect_db, send_response

# from functools import lru_cache

admin_route = APIRouter()

# @admin_route.get('/info/')
# async def get_db_info():
#     pass


@admin_route.post("/sets/", status_code=status.HTTP_204_NO_CONTENT)
async def update_set_info():
    conn, cur = connect_db()

    for sets in send_response("GET", "https://api.scryfall.com/sets")["data"]:
        cur.execute(
            """
            INSERT INTO card_info.sets (set, set_full, release_date)
            VALUES (%s, %s, %s)

            ON CONFLICT DO NOTHING
            """,
            (sets["code"], sets["name"], sets["released_at"]),
        )
    conn.commit()
    print("Hello, Sets are updated!")

    # for sets in BaseSetup.send_response("GET", "https://api.scryfall.com/sets")[


#     "data"
# ]:
#     if not sets["digital"]:
#         log.debug(f"Inserting {sets['name']} into card_info.sets")
#         self.cur.execute(
#             """
#             INSERT INTO card_info.sets (set, set_full, release_date)
#             VALUES (%s, %s, %s)

#             ON CONFLICT DO NOTHING
#             """,
#             (sets["code"], sets["name"], sets["released_at"]),
#         )
#         continue
