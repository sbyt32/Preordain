import logging
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import Session
from ..config import DB_HOST, DB_USER, DB_PASS, DB_NAME

log = logging.getLogger()

try:
    __database_connection_v2 = create_engine(
        URL.create(
            "postgresql+psycopg",
            username=str(DB_USER),
            password=str(DB_PASS),
            host=str(DB_HOST),
            database=str(DB_NAME),
        )
    )

    session = Session(__database_connection_v2)
    log.info("Database Connection should be successful!")
except Exception as e:
    log.critical(f"Database Connection Failed! Error: {e}")
    quit()
