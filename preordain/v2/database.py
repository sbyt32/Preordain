import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from ..config import DB_HOST, DB_USER, DB_PASS, DB_NAME

log = logging.getLogger()

try:
    __database_connection_v2 = create_engine(
        f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    )

    session = Session(__database_connection_v2)
except:
    log.critical("Database Connection Failed!")
    quit()
