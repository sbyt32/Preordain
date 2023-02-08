from fastapi import Header
from preordain.exceptions import TokenError
from preordain import config
import logging
log = logging.getLogger()

#  = Header() makes it so it has to pass through a header rather than a string

# ? All routes.
async def select_access(access: str):
    if access != str(config.SEC_TOKEN):
        raise TokenError("access")

# ? Admin route.
async def write_access(write_access: str = Header()):
    if write_access != str(config.WRITE_TOKEN):
        raise TokenError('write')

# ?  Price route.
async def price_access(price_access: str = Header()):
    if price_access != str(config.PRICE_TOKEN):
        raise TokenError('price')
