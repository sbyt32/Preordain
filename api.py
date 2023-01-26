import os
from fastapi import FastAPI, Response, status
from api_files.exceptions import TokenError, token_exception_handler

# ? Can I wrap this up in something more compact?
from api_files.routers.data import data_router
from api_files.routers.internal import internal_router

# * Logging Information
import logging
# ? For some reason, scripts/config_reader.py having the logging setup works fine. Need to know why eventually. Commented out for now
# import logging_details
# logging_details.log_setup()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# * Accessing the database should require the select_access token
app = FastAPI()
app.include_router(data_router.router)
app.include_router(internal_router.router)

@app.get("/", tags=["Test Connection"])
async def root(response: Response):
    if os.path.exists('config_files/config.ini'):
        return {
            "resp": "error",
            "status": 200,
            "message": "The request failed due to being at root. If you're just testing if it works, yeah it works.",
        }
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'resp'  :   'error',
            'status':   response.status_code,
            'detail':   'Configuration file improperly configured. Script will not function.'
        }

# ? Can this be done more efficently?
app.add_exception_handler(TokenError, token_exception_handler)