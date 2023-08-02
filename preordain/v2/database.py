import logging
from sqlalchemy import create_engine
from ..config import DB_HOST, DB_USER, DB_PASS, DB_NAME

log = logging.getLogger()

try:
    database_connection_v2 = create_engine(
        f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    )
except:
    log.critical("Database Connection Failed!")
    quit()
