import logging
import os

from fastapi import Request, status
from fastapi.responses import JSONResponse

from preordain.models import BaseResponse

log = logging.getLogger()

class PreordainException(Exception):
    resp: str
    status_code: int
    info: dict[str,str]

class BadToken(PreordainException):
    def __init__(self, token:str) -> None:
        self.token = token
        self.info = {
            "message": f"{token}_TOKEN was not given or was incorrect.",
        }
    resp = "invalid_token"
    status_code = status.HTTP_403_FORBIDDEN

class RootException(PreordainException):
    def __init__(self) -> None:
        if os.path.exists(".env"):
            self.status_code = status.HTTP_400_BAD_REQUEST
            self.info = {
                "message": "The request failed due to being at root. If you're just testing if it works, yeah it works.",
            }
        else:
            self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.info = {
                "message": "No .env file. Please run set_up.py.",
            }
    resp = "root_error"

class NotFound(PreordainException):
    resp = 'no_results'
    status_code = status.HTTP_403_FORBIDDEN
    info = {
        "message": "No results found"
    }

async def not_found_exception_handler(request: Request, exc: NotFound):
    log.warning(exc.info['message'])
    return JSONResponse(
        status_code=exc.status_code,
        content=BaseResponse(resp=exc.resp, status=exc.status_code, info=exc.info).dict(),
    )

async def token_exception_handler(request: Request, exc: BadToken):
    log.error(exc.info['message'])
    return JSONResponse(
        status_code=exc.status_code,
        content=BaseResponse(resp=exc.resp, status=exc.status_code, info=exc.info).dict(),
    )

async def root_exception_handler(request: Request, exc: RootException):
    log.warning('User accessed Root, did you mean to enter the Docs?')
    return JSONResponse(
        status_code=exc.status_code,
        content=BaseResponse(resp=exc.resp, status=exc.status_code, info=exc.info).dict()
    )