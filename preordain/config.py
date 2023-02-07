from starlette.config import Config
from starlette.datastructures import Secret
"""
    A way to read the .env file
"""
config = Config('.env')

DB_EXISTS = config('DB_EXISTS', cast=bool)
DB_HOST = config('DB_HOST', cast=Secret)
USER = config('USER', cast=Secret)
PASSWORD = config('PASSWORD', cast=Secret)
TCG_SALES = config('TCG_SALES', cast=str) # ? So, it's first a string, then needs to be cast as a datetime

SEC_TOKEN = config('SEC_TOKEN', cast=Secret)
WRITE_TOKEN = config('WRITE_TOKEN', cast=Secret)
PRICE_TOKEN = config('PRICE_TOKEN', cast=Secret)

DB_NAME = config('DB_NAME', cast=Secret)
TESTING = config('TESTING', cast=bool)
if TESTING:
    DB_NAME = Secret('test_' + str(DB_NAME))