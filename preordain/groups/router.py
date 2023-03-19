from fastapi import APIRouter, Response, status
from typing import Optional
from preordain.groups.models import GroupResponse, GroupInformation
from preordain.groups.schema import GroupInfoTable
from preordain.exceptions import NotFound
from preordain.utils.connections import connect_db
import logging

user_groups = APIRouter(
    responses={
        200: {
            "model": GroupResponse,
            "description": "Return the groups that the data is associated with.",
        }
    }
)
admin_groups = APIRouter()
log = logging.getLogger()


@user_groups.get(
    "/",
)
async def get_group_names(response: Response, in_use: Optional[bool] = False):
    """
    Returns the lists of groups
    Default returns all groups
    ```python
    in_use: bool
    ```
    """
    if in_use:
        query = """
        SELECT
            DISTINCT(group_in_use) AS "group",
            groups.description,
            a.qty as cards_in_group
        FROM (
            SELECT
                UNNEST(groups),
                COUNT(*) as qty
            FROM
            card_info.info
            GROUP BY UNNEST(groups)
            ) AS a(group_in_use)
        JOIN card_info.groups AS groups
            ON groups.group_name = group_in_use
        ORDER BY group_in_use ASC
    """
    else:
        query = """

        SELECT
            groups.group_name as "group",
            groups.description,
            CASE WHEN a.qty is NULL THEN 0 ELSE a.qty END as cards_in_group
        FROM (
            SELECT
                UNNEST(groups),
                COUNT(*) as qty
            FROM
            card_info.info
            GROUP BY UNNEST(groups)
            ) AS a(group_in_use)
        FULL OUTER JOIN card_info.groups AS groups
            ON groups.group_name = group_in_use

    """
    conn, cur = connect_db()
    cur.execute(query)
    data = cur.fetchall()
    conn.close()
    if data:
        response.status_code = status.HTTP_200_OK
        return GroupResponse(status=response.status_code, data=data)
    raise NotFound


@user_groups.post("/new/")
def add_new_group(group: GroupInfoTable):
    conn, cur = connect_db()

    # Insert group into card_info.group if not a duplicate.
    # Find way to return error if exists.
    cur.execute(
        """
        INSERT INTO card_info.groups
        VALUES (%(group_name)s, %(description)s)
        ON CONFLICT (group_name) DO NOTHING
        """,
        group.dict(),
    )
    pass


# @admin_groups.post("/add/")
# async def add_card_to_groups(card_group: CardInGroupInfo):
#     text_resp = ""

#     conn, cur = connect_db()

#     cur.execute(
#         "SELECT name, set, id, groups from card_info.info where id = %s AND set= %s",
#         (card_group.id, card_group.set),
#     )

#     fetched_card = cur.fetchone()
#     # * If the card doesn't already have a group, it'll return Null/None.
#     if fetched_card["groups"] is None:
#         fetched_card["groups"] = []

#     # * If the card exists and the group is not associated with the card.
#     if fetched_card and not card_group.group in fetched_card["groups"]:
#         cur.execute(
#             "UPDATE card_info.info SET groups = array_append(card_info.info.groups, %s) WHERE id = %s and set = %s",
#             (card_group.group, card_group.id, card_group.set),
#         )
#         conn.commit()

#         text_resp = f"{fetched_card['name']} (Set: {fetched_card['set']}, Collector Num: {fetched_card['id']}) is now associated with the groups: {fetched_card['groups'] + [card_group.group]}"
#         log.info(text_resp)

#     # * Warning if the group is already with the card
#     elif card_group.group in fetched_card["groups"]:
#         text_resp = f"{fetched_card['name']} (Set: {fetched_card['set']}, Collector Num: {fetched_card['id']}) already is associated with the group: {fetched_card['groups']}"
#         log.warning(text_resp)

#     # * If the card doesn't exist on the database. It might exist as a card, though.
#     elif fetched_card == None:
#         text_resp = f"Set: {card_group.set}, Collector Num: {card_group.id} does not exist on the database!"
#         log.error(text_resp)

#     # * Just in case, I'm not too sure what would trigger this?
#     else:
#         text_resp = f"Uncertain error returned. Logging response to look over later."
#         log.error(card_group)

#     return text_resp


# @admin_groups.delete("/remove/")
# async def remove_card_from_group(card_group: CardInGroupInfo):
#     conn, cur = connect_db()

#     cur.execute(
#         "SELECT name, set, id, groups from card_info.info where id = %s AND set= %s",
#         (card_group.id, card_group.set),
#     )

#     fetched_card = cur.fetchone()

#     # * If the card exists and the group is associated with the card.
#     if fetched_card and card_group.group in fetched_card["group"]:
#         cur.execute(
#             "UPDATE card_info.info SET groups = array_remove(card_info.info.groups, %s) WHERE id = %s and set = %s",
#             (card_group.group, card_group.id, card_group.set),
#         )
