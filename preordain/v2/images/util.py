import requests, os, shutil, logging
from typing import Union
from preordain.config import IMG_FOLDER_PATH_V2
from cachetools import cached, LRUCache

log = logging.getLogger()


@cached(cache=LRUCache(maxsize=64))
def get_image_path(scryfall_uri: str, type: str) -> Union[str, None]:
    url = f"https://api.scryfall.com/cards/{scryfall_uri}?format=image"
    print(url)
    # TODO: add image banner
    img_path = f"{IMG_FOLDER_PATH_V2.format(scryfall_uri=scryfall_uri)}.jpg"
    if not os.path.exists(img_path):
        log.warning(f"Missing image {scryfall_uri}, downloading...")
        card_img = requests.request(method="GET", url=url, stream=True)
        if not card_img.ok:
            log.error(f"Failed to get image: {scryfall_uri}")
            return None

        with open(img_path, "wb") as write_img:
            card_img.raw.decode_content = True
            shutil.copyfileobj(card_img.raw, write_img)

    return img_path
