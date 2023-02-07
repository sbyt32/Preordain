import os
from fastapi import FastAPI, Response, status
from preordain.exceptions import TokenError, token_exception_handler
from fastapi.middleware.cors import CORSMiddleware
from preordain.information.router import user_router as info_user_router
from preordain.information.router import admin_router as info_admin_router
from preordain.information.router import search_router as info_search_router
from preordain.inventory.router import router as inventory_router
from preordain.price_sales.router import price_router
from preordain.price_sales.router import sale_router
from preordain.groups.router import router as groups_router

# * Logging Information
import logging
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# * Accessing the database should require the select_access token
app = FastAPI()

# ? I really don't like this out in the open, but I'm leaving it here for testing. 
origins = [
    "http://localhost.tiangolo.com",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(info_admin_router)
app.include_router(info_user_router)
app.include_router(info_search_router)
app.include_router(inventory_router)
app.include_router(price_router)
app.include_router(sale_router)
app.include_router(groups_router)


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