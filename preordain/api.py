import os
from fastapi import Response, status, Depends, APIRouter
from preordain.dependencies import select_access, write_access
from preordain.models import BaseResponse

from preordain.groups.router import admin_groups as groups_admin_router
from preordain.groups.router import user_groups as groups_user_router
from preordain.price.router import price_router
from preordain.information.router import admin_router as info_admin_router
from preordain.information.router import user_router as info_user_router
from preordain.information.models import CardInformation
from preordain.inventory.router import router as inventory_router
from preordain.sales.router import sale_router
from preordain.search.router import search_router

api_router = APIRouter(
    responses={
        404: {
            "model": BaseResponse,
            "description": "Not Found",
            "content": {
                "application/json": {
                    "example": {
                        "resp": "no_results",
                        "status": 404,
                        "info": {"message": "No Results Found!"},
                    }
                }
            },
        }
    }
)

# * User Stuff
api_router.include_router(
    info_user_router,
    prefix="/card",
    tags=["Card Information, etc"],
    responses={200: {"model": BaseResponse[CardInformation]}},
)
api_router.include_router(
    search_router,
    prefix="/search",
    tags=["Search for a card"],
    responses={200: {"model": BaseResponse[CardInformation]}},
)
api_router.include_router(
    inventory_router,
    prefix="/inventory",
    tags=["Inventory Management"],
    dependencies=[Depends(select_access)],
    # responses={200: {'model': BaseResponse[InventoryData]}}
)
api_router.include_router(
    price_router,
    prefix="/price",
    tags=["Get Prices (from Scryfall)"],
    # responses={200: {'model': BaseResponse}}
)
api_router.include_router(
    sale_router, prefix="/sales", tags=["Get Sales (From TCGPlayer)"]
)
api_router.include_router(
    groups_user_router,
    prefix="/groups",
    tags=["Card Groups"],
)

# # * Admin Panel
api_router.include_router(
    groups_admin_router,
    prefix="/groups",
    tags=["Card Groups"],
    dependencies=[Depends(write_access)],
)
api_router.include_router(
    info_admin_router,
    prefix="/admin",
    tags=["Admin Panel"],
    dependencies=[Depends(write_access)],
)


@api_router.get("/", tags=["Test Connection"])
async def root(response: Response):
    if os.path.exists(".env"):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "resp": "root_error",
            "status": response.status_code,
            "info": {
                "message": "The request failed due to being at root. If you're just testing if it works, yeah it works."
            },
        }
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "resp": "root_error",
            "status": response.status_code,
            "info": {
                "message": "Configuration file improperly configured. Script will not function."
            },
        }
