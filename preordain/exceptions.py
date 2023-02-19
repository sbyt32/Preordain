import logging

from fastapi import Request, status
from fastapi.responses import JSONResponse

from preordain.models import BaseError, RespStrings

log = logging.getLogger()


class PreordainException(Exception):
    resp: RespStrings
    status: int
    info: dict[str, str]


class NotFound(PreordainException):
    resp = RespStrings.no_results
    status = status.HTTP_404_NOT_FOUND
    info = {"message": "No results found."}


async def not_found_exception_handler(request: Request, exc: NotFound):
    log.warning(exc.info["message"])
    exc = NotFound
    return JSONResponse(
        status_code=exc.status,
        content=BaseError(**dict(**exc.__dict__)).dict(),
    )


class InvalidToken(PreordainException):
    def __init__(self, token: str) -> None:
        self.token = token.upper()
        self.info = {
            "message": f"{self.token}_TOKEN was not given or was incorrect.",
        }

    resp = "invalid_token"
    status_code = status.HTTP_403_FORBIDDEN


async def token_exception_handler(request: Request, exc: InvalidToken):
    log.error(exc.info["message"])
    return JSONResponse(
        status_code=exc.status_code,
        content=BaseError(resp=exc.resp, status=exc.status_code, info=exc.info).dict(),
    )


class RootException(PreordainException):
    def __init__(self) -> None:
        self.info = {
            "message": "The request failed due to being at root. If you're just testing if it works, yeah it works.",
        }

    status_code = status.HTTP_400_BAD_REQUEST
    resp = "root_error"


async def root_exception_handler(request: Request, exc: RootException):
    log.warning("User accessed Root, did you mean to enter the Docs?")
    return JSONResponse(
        status_code=exc.status_code,
        content=BaseError(resp=exc.resp, status=exc.status_code, info=exc.info).dict(),
    )
