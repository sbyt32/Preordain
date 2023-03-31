from starlette.config import Config, environ
from starlette.datastructures import Secret
from dateutil.relativedelta import relativedelta

from .logging_details import log_setup
import logging
import sys

log_setup()
log = logging.getLogger("preordain")

"""
    A way to read the .env file
"""
try:
    config = Config(".env")
    PROJECT = config("PROJECT", cast=str, default="Preordain")
    DB_EXISTS = config("DB_EXISTS", cast=bool)
    DB_HOST = config("DB_HOST", cast=Secret)
    DB_USER = config("DB_USER", cast=Secret)
    DB_PASS = config("DB_PASS", cast=Secret)
    DB_NAME = config("DB_NAME", cast=Secret)

    TCG_SALES = config("TCG_SALES", cast=str)
    # ? So, it's first a string, then needs to be cast as a datetime

    SEC_TOKEN = config("SEC_TOKEN", cast=Secret)
    WRITE_TOKEN = config("WRITE_TOKEN", cast=Secret)
    PRICE_TOKEN = config("PRICE_TOKEN", cast=Secret)

    # * Keep the days the same, this is to make sure that the database has time to scrape the data.
    UPDATE_OFFSET = relativedelta(days=+1, hour=0, minute=10, second=0, microsecond=0)

    TESTING = config("TESTING", cast=bool)
    if TESTING:
        DB_NAME = Secret("test_" + str(DB_NAME))

except KeyError as e:
    if not environ.get("TESTING"):
        log.critical(e)
        sys.exit(1)
