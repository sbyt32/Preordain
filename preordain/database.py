import requests
import logging
from typing import Union
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import Session
from .config import DB_HOST, DB_USER, DB_PASS, DB_NAME

log = logging.getLogger()


def send_request(method: str, url: str, **kwargs) -> Union[list, dict, None]:
    log.debug(f"Sending a {method} request to {url} with kwargs: {kwargs or 'N/A'}")
    req = requests.request(method, url, **kwargs)

    if req.ok:
        response: Union[list, dict] = req.json()
        return response

    log.error(f"Request Failed! Status Code: {req.status_code}")


try:
    database_engine_v2 = create_engine(
        URL.create(
            "postgresql+psycopg",
            username=str(DB_USER),
            password=str(DB_PASS),
            host=str(DB_HOST),
            database=str(DB_NAME),
        )
    )

    session = Session(database_engine_v2)
    log.info("Database Connection should be successful!")
except Exception as e:
    log.critical(f"Database Connection Failed! Error: {e}")
    quit()
