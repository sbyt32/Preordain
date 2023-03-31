from fastapi import APIRouter, Response, status
from typing import Optional
from preordain.groups.models import (
    ShowGroupResponse,
    CardInGroupInfo,
    SuccessfulRequest,
)
from preordain.groups.models import SingleGroupResponse
from preordain.groups.schema import GroupInfoTable
from preordain.groups.util import validate_group
from preordain.exceptions import NotFound
from preordain.utils.connections import connect_db
from preordain.utils.parsers import parse_data_for_response

user_groups = APIRouter()


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
        return ShowGroupResponse(status=response.status_code, data=data)
    raise NotFound


@user_groups.get("/{group}", description="Filter for cards by their groups.")
async def find_by_group(group: str, response: Response):
    conn, cur = connect_db()
    cur.execute(
        """

        SELECT
            DISTINCT ON (info.name, info.id, info.set) "name",
            info.set,
            sets.set_full,
            info.id,
            info.uri,
            prices.date AS "date",
            prices.usd,
            prices.usd_foil,
            prices.usd_etch,
            prices.euro,
            prices.euro_foil,
            prices.tix
        FROM card_info.info AS "info"
        JOIN card_info.sets AS "sets"
            ON info.set = sets.set
        JOIN
            (
                SELECT
                    prices.date,
                    prices.uri,
                    prices.usd,
                    prices.usd_foil,
                    prices.usd_etch,
                    prices.euro,
                    prices.euro_foil,
                    prices.tix
                FROM
                    card_data as "prices"
                WHERE prices.date = (SELECT MAX(date) as last_update from card_data)
            ) AS "prices"
        ON prices.uri = info.uri
        WHERE %s = ANY (info.groups)
        ORDER BY
            info.name,
            info.id,
            info.set,
            prices.date DESC

        """,
        (group,),
    )
    data = cur.fetchall()
    cur.execute(
        """
        SELECT
            groups.group_name,
            groups.description,
            (SELECT COUNT(*) AS QTY FROM card_info.info WHERE %s = ANY(groups))
        FROM card_info.groups AS groups
        WHERE %s = groups.group_name
    """,
        (
            group,
            group,
        ),
    )
    info = cur.fetchone()
    conn.close()
    if data:
        response.status_code = status.HTTP_200_OK
        return SingleGroupResponse(
            info=info, status=response.status_code, data=parse_data_for_response(data)
        )

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
        info={"message": f"Added group: {group.group_name}"},
        data=group,
    )


@user_groups.delete("/delete/{group}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(group: str):
    conn, cur = connect_db()
    cur.execute(
        """
        DELETE FROM card_info.groups WHERE group_name = %s
        """,
        (group,),
    )
    conn.commit()
    conn.close()


@user_groups.post(
    "/add/card/",
    response_model=SuccessfulRequest,
    status_code=status.HTTP_201_CREATED,
)
async def add_card_to_groups(card_group: CardInGroupInfo):
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
        card_data,
    )
    conn.commit()
    return SuccessfulRequest(
        status=status.HTTP_201_CREATED,
        info={"message": f"Successfully added card to {card_data['group']}"},
    )


@user_groups.post(
    "/remove/card/", response_model=SuccessfulRequest, status_code=status.HTTP_200_OK
)
async def remove_card_from_group(card_group: CardInGroupInfo):
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
    return SuccessfulRequest(
        status=status.HTTP_200_OK,
        info={"message": f"Successfully removed card from {card_data['group']}"},
    )
