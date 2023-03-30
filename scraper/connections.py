import psycopg
from psycopg.rows import dict_row
import requests
import logging
from typing import Union
import os

log = logging.getLogger()


def connect_db():
    DB_HOST = os.environ.get("DB_HOST") or "plateau"
    DB_USER = os.environ.get("DB_USER") or "coyote"
    DB_PASS = os.environ.get("DB_PASS") or "whywhy22"
    DB_NAME = os.environ.get("DB_NAME") or "test_ratio_lol"

    """Always have two variables into this, connection and cursor. Default to `conn, cur = connect_db`
    \n[More info about psycopg](https://www.psycopg.org/psycopg3/docs/api/connections.html#psycopg.Connection)
    """
    print(DB_HOST)
    db_info = dict(
        zip(
            ("host", "user", "password", "dbname"),
            (
                DB_HOST,
                DB_USER,
                DB_PASS,
                DB_NAME,
            ),
        )
    )
    conn_info = psycopg.conninfo.make_conninfo(**db_info)

    log.debug(f"Connecting to database: {db_info['dbname']}")
    try:
        conn = psycopg.connect(conn_info, row_factory=dict_row)
    except psycopg.OperationalError as e:
        raise Exception(e)
    cur = conn.cursor()

    return conn, cur


def send_response(method: str, url: str, **kwargs) -> Union[list, dict, None]:
    r = requests.request(method, url, **kwargs)
    log.debug(f"Sending a {method} to {url} with kwargs: {kwargs}")
    if not r.ok:
        # todo: Add logging issue
        # log.error(f"Request failed! Status code:{r.status_code}")
        log.exception(f"Request failed! Status code:{r.status_code}")
    else:
        response: Union[list, dict] = r.json()
        return response
