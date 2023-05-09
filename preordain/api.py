from fastapi import Depends, APIRouter
from preordain.dependencies import select_token, write_token
from preordain.utils.find_missing import validate_table_data
from preordain.models import BaseError, RespStrings, RootResponse
from preordain.exceptions import RootException
from preordain.events.router import router as events_router
from preordain.groups.router import user_groups as groups_user_router
from preordain.price.router import price_router
from preordain.price.models import PriceDataMultiple, PriceDataSingle, PriceChange
from preordain.internal.router import admin_route as internal_router
from preordain.information.router import user_router as info_user_router
from preordain.information.models import CardInformation
from preordain.inventory.router import router as inventory_router
from preordain.inventory.router import InventoryResponse
from preordain.sales.router import sales_router
from preordain.sales.models import CardSaleResponse
from preordain.search.router import search_router
from preordain.search.models import SearchInformation
from preordain.tracker.router import router as tracker_router
from preordain.config import PROJECT
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
            "description": "Successful Request",
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

api_router.include_router(
    internal_router,
    prefix="/admin",
    tags=["Administrative Stuff"],
    dependencies=[Depends(write_token)],
)

api_router.include_router(events_router, prefix="/events", tags=["Get Event Data"])


@api_router.get(
    "/",
    tags=["Test Connection"],
    status_code=200,
    responses={200: {"model": RootResponse, "description": "Testing Root"}},
)
async def root():
    checks = validate_table_data()
    return RootResponse(
        status=200,
        info={
            "message": f"Welcome to {PROJECT}! The following is the checks that is needed for data to show up. If any are false, that might be why nothing is displaying.",
            "checks": {
                "Set Information": checks["info_exists"],
                "Price Data (at least one days worth)": checks["price_exists"],
            },
        },
    )
