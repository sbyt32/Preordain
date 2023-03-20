from psycopg import Cursor


def validate_group(cur: Cursor, card_data: dict):
    cur.execute(
        """SELECT
        EXISTS (SELECT group_name FROM card_info.groups WHERE group_name = %(group)s) AS group_exists,
        EXISTS (SELECT name from card_info.info WHERE %(group)s = ANY(groups) AND uri = %(uri)s) AS card_in_group
        """,
        card_data,
    )
    return cur.fetchone()
