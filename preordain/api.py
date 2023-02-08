import os
from fastapi import FastAPI, Response, status, Depends
from fastapi.middleware.cors import CORSMiddleware

from preordain.logging_details import log_setup
from preordain.exceptions import TokenError, token_exception_handler
from preordain.information.router import user_router as info_user_router
from preordain.information.router import admin_router as info_admin_router
from preordain.search.router import search_router
from preordain.inventory.router import router as inventory_router
from preordain.price_sales.router import price_router
from preordain.price_sales.router import sale_router
from preordain.groups.router import user_groups as groups_user_router
from preordain.groups.router import admin_groups as groups_admin_router
from preordain.dependencies import select_access, write_access

# * Logging Information
log_setup()
import logging
log = logging.getLogger()
log.setLevel(logging.DEBUG)

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

# * User Stuff
app.include_router(
    info_user_router,
    prefix="/card",
    tags=["Card Information, etc"]
    )
app.include_router(
    search_router,
    prefix='/search',
    tags=["Search for a card"]
)
app.include_router(
    inventory_router,     
    prefix="/inventory",
    tags=["Inventory Management"],
    dependencies=[Depends(select_access)]
)
app.include_router(
    price_router,     
    prefix="/price",
    tags=["Get Prices (from Scryfall)"]
)
app.include_router(sale_router,
    prefix="/sales",
    tags=["Get Sales (From TCGPlayer)"]
)
app.include_router(
    groups_user_router,
    prefix="/groups",
    tags=["Card Groups"],
)

# * Admin Panel
app.include_router(
    groups_admin_router,
    prefix="/groups",
    tags=["Card Groups"],
)
app.include_router(
    info_admin_router,
    prefix="/admin",
    tags=["Admin Panel"],
    dependencies=[Depends(write_access)]
)

@app.get("/", tags=["Test Connection"])
async def root(response: Response):
    if os.path.exists('.env'):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "resp": "error",
            "status": response.status_code,
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