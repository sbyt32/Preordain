from fastapi import Depends, APIRouter
from preordain.dependencies import select_token, write_token
from preordain.models import BaseError, RespStrings
from preordain.exceptions import RootException
from preordain.groups.router import admin_groups as groups_admin_router
from preordain.groups.router import user_groups as groups_user_router
from preordain.price.router import price_router
from preordain.price.models import PriceDataMultiple, PriceDataSingle, PriceChange
from preordain.information.router import user_router as info_user_router
from preordain.information.models import CardInformation
from preordain.inventory.router import router as inventory_router
from preordain.inventory.router import InventoryResponse
from preordain.sales.router import sales_router
from preordain.sales.models import CardSaleResponse
from preordain.search.router import search_router
from preordain.search.models import SearchInformation
from preordain.trackers.router import router as tracker_router

from typing import Union

api_router = APIRouter(
    responses={
        404: {
            "model": BaseError,
            "description": "Not Found",
            "content": {
                "application/json": {
                    "example": {
                        "resp": RespStrings.no_results,
                        "status": 404,
                        "info": {"message": "No Results Found!"},
                    }
                }
            },
        },
        400: {
            "model": BaseError,
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {
                        "resp": RespStrings.error_request,
                        "status": 400,
                        "info": {"message": "Unable to process Request"},
                    }
                }
            },
        },
    }
)

# * User Stuff
api_router.include_router(
    info_user_router,
    prefix="/card",
    tags=["Card Information, etc"],
    responses={
        200: {
            "model": CardInformation,
            "description": "Return the groups that the data is associated with.",
        }
    },
)
api_router.include_router(
    search_router,
    prefix="/search",
    tags=["Search for a card"],
    responses={200: {"model": SearchInformation}},
)
api_router.include_router(
    inventory_router,
    prefix="/inventory",
    tags=["Inventory Management"],
    dependencies=[Depends(select_token)],
    responses={200: {"model": InventoryResponse}},
)
api_router.include_router(
    price_router,
    prefix="/price",
    tags=["Get Prices (from Scryfall)"],
    responses={200: {"model": Union[PriceDataSingle, PriceDataMultiple, PriceChange]}},
)
api_router.include_router(
    sales_router,
    prefix="/sales",
    tags=[
        "Get Sales (From TCGPlayer)",
    ],
    responses={200: {"model": CardSaleResponse}},
)
api_router.include_router(
    groups_user_router,
    prefix="/groups",
    tags=["Card Groups"],
)
api_router.include_router(
    tracker_router,
    prefix="/tracker",
    tags=["Update Data (needs token)"],
    dependencies=[Depends(write_token)],
)

# # # * Admin Panel
# api_router.include_router(
#     groups_admin_router,
#     prefix="/groups",
#     tags=["Card Groups"],
#     dependencies=[Depends(write_access)],
# )
# api_router.include_router(
#     info_admin_router,
#     prefix="/admin",
#     tags=["Admin Panel"],
#     dependencies=[Depends(write_access)],
# )


@api_router.get("/", tags=["Test Connection"])
async def root():
    raise RootException
