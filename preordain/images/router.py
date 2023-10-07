from fastapi import APIRouter, Response, status
from fastapi.responses import FileResponse
from cachetools import cached, LRUCache
from preordain.images.util import get_image_path

img_router = APIRouter()


@cached(cache=LRUCache(64))
@img_router.get(
    "/{scryfall_uri}", response_class=FileResponse, status_code=status.HTTP_200_OK
)
async def get_img(scryfall_uri: str):
    return get_image_path(scryfall_uri, "")
