from api_files.routers.data.card_tracking_scripts import return_card_info
from fastapi import APIRouter, Depends
from api_files.dependencies import select_access

router = APIRouter(
    prefix="/card",
    tags=["Get some card info"],
    dependencies=[Depends(select_access)],
    responses={404: {"description": "Not found"}},
)

router.include_router(return_card_info.router)
