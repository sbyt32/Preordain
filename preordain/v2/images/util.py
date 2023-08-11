from preordain.config import IMG_FOLDER_PATH_V2
from database import send_request
from cachetools import cached, LRUCache


@cached(cache=LRUCache(maxsize=64))
def get_image_path(scryfall_uri: str, type: str):
    url = f"https://api.scryfall.com/cards/{scryfall_uri}?format=image"
    # TODO: add image banner
    IMG_FOLDER_PATH_V2.format(scryfall_uri)

    pass
