import logging
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
app = FastAPI()
log = logging.getLogger()


# TODO: make an exception that mimics the Scryfall API response for the root error 
"""
{
  "object": "error",
  "code": "bad_request",
  "status": 400,
  "details": "This is the root of the Scryfall API and no data is returned at this path. For more information about the methods and objects this API publishes, please see https://scryfall.com/docs/api"
}
"""

# Failed Token
class TokenError(Exception):
    def __init__(self, token:str):
        self.token = token
        log.error(f"Recieved incorrect or no {self.token}_token")

@app.exception_handler(TokenError)
async def token_exception_handler(request: Request, exc: TokenError):
    return JSONResponse(
        status_code=403,
        content={
            "resp": "error",
            "status": 403,
            "message": f"{exc.token}_token was not given or was incorrect. This error has been logged.",
        }
    )

class BadResponseException(Exception):
    def __init__(self, error):
        self.error = error

@app.exception_handler(BadResponseException)
async def bad_response_exception_handler(request: Request, exc: BadResponseException):
    return JSONResponse(
        status_code=400,
        content={
            "resp": "error",
            "status": 400,
            "message": f"{exc.error}"
        }
    )