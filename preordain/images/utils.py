from preordain.config import FOLDER_PATH
from preordain.utils.find_missing import get_card_from_set_id
from preordain.images.enums import ImageTypes
import requests, os, shutil


def get_img_path(set: str, col_num: str, type: ImageTypes = ImageTypes.cards):
    url = f"https://api.scryfall.com/cards/{set}/{col_num}?format=image"
    if type == ImageTypes.banner:
        url += "&version=art_crop"
    folder_path = FOLDER_PATH.format(set=set, type=type)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    image_path = f"{folder_path}{get_card_from_set_id(set, col_num)}.jpg"
    if not os.path.exists(image_path):
        card_image = requests.request(
            method="GET",
            url=url,
            stream=True,
        )
        with open(image_path, "wb") as write_img:
            card_image.raw.decode_content = True
            shutil.copyfileobj(card_image.raw, write_img)

    return image_path
