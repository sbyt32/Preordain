from fastapi import APIRouter, Response, status, Body
from typing import Optional
from preordain.groups.models import (
    GroupResponse,
    CardInGroupInfo,
    SuccessfulRequest,
    GroupInfoTable,
)
from preordain.groups.schema import GroupInfoGroupName
from preordain.exceptions import NotFound
from preordain.groups.util import validate_group
from preordain.utils.connections import connect_db
import logging
from typing import Annotated

user_groups = APIRouter()
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
def add_group(group: GroupInfoTable, response: Response):
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
    conn.commit()
    response.status_code = status.HTTP_201_CREATED
    return SuccessfulRequest(
        status=response.status_code,
        info={"Message": f"Added group: {group.group_name}"},
        data=group,
    )


@user_groups.delete("/delete/")
async def delete_group(response: Response, group: GroupInfoGroupName):
    conn, cur = connect_db()
    cur.execute(
        """
        DELETE FROM card_info.groups WHERE group_name = %(group_name)s
        """,
        group.dict(),
    )
    conn.commit()
    response.status_code = status.HTTP_200_OK
    return SuccessfulRequest(
        status=response.status_code,
        info={"message": f"Removed group: {group.group_name}"},
        data=group,
    )


@user_groups.post(
    "/add/card/",
    response_model=SuccessfulRequest,
    responses={
        201: {
            "model": SuccessfulRequest,
            "description": "Successfully Added to Group",
            "content": {
                "application/json": {
                    "example": {
                        "resp": "group_info",
                        "status": 201,
                        "info": {
                            "message": "Successfully added card to Death and Taxes"
                        },
                    }
                }
            },
        }
    },
)
async def add_card_to_groups(card_group: CardInGroupInfo, response: Response):
    conn, cur = connect_db()
    card_data = card_group.dict()

    pre_check = validate_group(cur, card_data)
    # Write some exceptions.
    if not pre_check["group_exists"]:
        raise Exception("Hey, Group Does Not Exist!")
    elif pre_check["card_in_group"]:
        raise Exception(f"This card is already in group: {card_data['group']}")

    cur.execute(
        "UPDATE card_info.info SET groups = array_append(card_info.info.groups, %(group)s) WHERE uri = %(uri)s",
        card_group.dict(),
    )
    conn.commit()
    response.status_code = status.HTTP_201_CREATED
    return SuccessfulRequest(
        status=response.status_code,
        info={"message": f"Successfully added card to {card_data['group']}"},
    )


@user_groups.delete("/remove/card/", response_model=SuccessfulRequest)
async def remove_card_from_group(card_group: CardInGroupInfo, response: Response):
    conn, cur = connect_db()
    card_data = card_group.dict()

    pre_check = validate_group(cur, card_data)
    # Write some exceptions.
    if not pre_check["group_exists"]:
        raise Exception("Hey, Group Does Not Exist!")
    elif not pre_check["card_in_group"]:
        raise Exception(f"This card is not in group: {card_data['group']}")

    cur.execute(
        "UPDATE card_info.info SET groups = array_remove(card_info.info.groups, %(group)s) WHERE uri = %(uri)s",
        card_data,
    )
    conn.commit()
    response.status_code = status.HTTP_200_OK
    return SuccessfulRequest(
        status=response.status_code,
        info={"message": f"Successfully removed card from {card_data['group']}"},
    )
