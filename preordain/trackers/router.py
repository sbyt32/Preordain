import logging

log = logging.getLogger()
from preordain.utils.connections import connect_db, send_response
from preordain.trackers.schema import CardInfoModel
from preordain.trackers.models import SuccessfulRequest
from preordain.trackers.dependencies import duplicate_card
from fastapi import APIRouter, Response, status, Depends

router = APIRouter()


@router.post("/add/", response_model=SuccessfulRequest)
async def add_card_to_track(
    response: Response, card: CardInfoModel = Depends(duplicate_card)
):
    card_dict = card.dict()
    conn, cur = connect_db()

    query = """
        INSERT INTO card_info.info (name, set, id, uri, tcg_id, tcg_id_etch, new_search)

        VALUES (%(name)s,%(set)s,%(id)s,%(uri)s,%(tcg_id)s,%(tcg_id_etch)s,%(new_search)s)
    """
    cur.execute(query, card_dict)
    conn.commit()
    conn.close()
    response.status_code = status.HTTP_201_CREATED

    return SuccessfulRequest(status=response.status_code, data=card)

    # try:
    #     if resp["object"] != "list":
    #         log.error("Not a card!")
    #         raise NotFound

    # except KeyError as e:
    #     # ? What does this look like, again?
    #     log.error(f"KeyError:{e}")

    # else:
    #     if resp["total_cards"] != 1:
    #         error_msg = f"Recieved list with more than 1. Set:{set}, ID:{col_num}"
    #         log.error(error_msg)
    #         return error_msg

    #     resp = resp["data"][0]
    #     conn, cur = connect_db()
    #     cur.execute(
    #         "SELECT * from card_info.info where id = %s AND set= %s",
    #         (resp["collector_number"], resp["set"]),
    #     )
    #     if (
    #         not cur.fetchall()
    #     ):  # * Run this section if no results (empty lists are False)
    #         if "tcgplayer_etched_id" in resp:
    #             tcg_etched_id = resp["tcgplayer_etched_id"]
    #         else:
    #             tcg_etched_id = None

    #         add_info_to_postgres = """
    #                 INSERT INTO card_info.info (name, set, id, uri, tcg_id, tcg_id_etch, new_search)

    #                 VALUES (%s,%s,%s,%s,%s,%s,%s)
    #                 """
    #         # ? Uncomment below in production.
    #         cur.execute(
    #             add_info_to_postgres,
    #             (
    #                 resp["name"],
    #                 resp["set"],
    #                 resp["collector_number"],
    #                 resp["id"],
    #                 resp["tcgplayer_id"],
    #                 tcg_etched_id,
    #                 True,
    #             ),
    #         )
    #         conn.commit()

    #         log.info(f'Now tracking: {resp["name"]} from {resp["set_name"]}')
    #         return f'Now tracking: {resp["name"]} from {resp["set_name"]}'

    #     else:
    #         log.info(f'Already tracking: {resp["name"]} from {resp["set_name"]}')
    #         return f'Already tracking: {resp["name"]} from {resp["set_name"]}'
