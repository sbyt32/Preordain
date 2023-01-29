from fastapi import APIRouter
from typing import Optional
from api_files.response_class.pretty import PrettyJSONResp
import scripts.connect.to_database as to_db
from psycopg.rows import dict_row

router = APIRouter()

# Return all group names in current use
@router.get("/", status_code=200, response_class=PrettyJSONResp)
async def get_group_names(use: Optional[bool]):
    if use:
        query = """
        SELECT 
            DISTINCT(group_in_use) AS "group",
            groups.description
        FROM (
            SELECT 
                UNNEST(groups) 
            FROM 
            card_info.info
            ) AS a(group_in_use)
        JOIN card_info.groups AS groups
            ON groups.group_name = group_in_use
    """
    else:
        query = """
        
        SELECT 
            groups.group_name,
            groups.description
        FROM card_info.groups AS groups
        
    """
    conn, cur = to_db.connect_db(row_factory = dict_row)

    cur.execute(query)
    return cur.fetchall()