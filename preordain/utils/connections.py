import psycopg
from psycopg.rows import dict_row
import requests
import logging
# from preordain.config_reader import read_config
from preordain import config
log = logging.getLogger()

def connect_db():
    """Always have two variables into this, connection and cursor. Default to `conn, cur = connect_db`    
    \n[More info about psycopg](https://www.psycopg.org/psycopg3/docs/api/connections.html#psycopg.Connection)
    """
    # db_info = read_config("CONNECT", 'database')
    db_info = dict(
        zip (   
            ('host','user', 'password', 'dbname'), 
            (str(config.DB_HOST), str(config.USER), str(config.PASSWORD), str(config.DB_NAME))
            )
        )
    log.debug(f"Connecting to database: {db_info['dbname']}")
    conn_info = psycopg.conninfo.make_conninfo(**db_info)
    
    conn = psycopg.connect(conn_info, row_factory=dict_row)
    cur  = conn.cursor()

    return conn, cur

def send_response(method:str, url:str, **kwargs):
    r = requests.request(method, url, **kwargs)
    log.debug(f'Sending a {method} to {url} with kwargs: {kwargs}')
    if not r.ok:
        # todo: Add logging issue
        log.error(f"Request failed! Status code:{r.status_code}")
        # return r.json()
        # raise 
    else:
        card_list = r.json()
        return card_list