from fastapi import Header
from preordain.exceptions import InvalidToken
from preordain import config

#  = Header() makes it so it has to pass through a header rather than a string


# ? All routes.
async def select_token(access: str):
    if access != str(config.SEC_TOKEN):
        raise InvalidToken(token="ACCESS")


# ? Admin route.
async def write_token(write: str = Header()):
    if write != str(config.WRITE_TOKEN):
        raise InvalidToken(token="WRITE")


# ?  Price route.
async def price_token(price: str = Header()):
    if price != str(config.PRICE_TOKEN):
        raise InvalidToken(token="PRICE")
