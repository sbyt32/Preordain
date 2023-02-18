from preordain.exceptions import PreordainException
from pydantic.errors import PydanticValueError
import logging
import os
from fastapi import Request,status
from fastapi.responses import JSONResponse
from preordain.models import BaseResponse
log = logging.getLogger()

class InvalidSearchQuery(PreordainException):
    info = {
            "message": "Recieved invalid string from user.",
    }
    resp = "error_request"
    status_code = status.HTTP_400_BAD_REQUEST

async def invalid_search_handler(request: Request, exc: InvalidSearchQuery):
    log.warning(exc.info['message'])
    return JSONResponse(
        status_code=exc.status_code,
        content=BaseResponse(resp=exc.resp, status=exc.status_code, info=exc.info).dict()
    )