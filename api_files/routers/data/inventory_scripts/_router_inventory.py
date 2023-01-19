from api_files.routers.data.inventory_scripts import return_inventory
from fastapi import APIRouter, Depends
from api_files.dependencies import select_access

router = APIRouter(
    prefix="/inventory",
    tags=["Manage your Inventory"],
    dependencies=[Depends(select_access)]
)

router.include_router(return_inventory.router)