import os
import requests
import shutil
from fastapi import APIRouter, Response, status
from preordain.utils.connections import connect_db
from preordain.utils.parsers import parse_data_for_response
from preordain.information.models import CardInformation, CardPurchaseLink
from preordain.exceptions import NotFound
from preordain.utils.find_missing import get_card_from_set_id
from fastapi.responses import FileResponse


user_router = APIRouter()


@user_router.get(
    "/{set}/{col_num}",
    description="Look for a specific card based on the set and collector number",
)
async def search_by_set_collector_num(set: str, col_num: str, response: Response):
    conn, cur = connect_db()
    uri = get_card_from_set_id(set, col_num)
    cur.execute(
        """
            SELECT
                info.name,
                info.set,
                sets.set_full,
                info.id,
                info.uri,
                price.date,
                price.usd,
                price.usd_foil,
                price.usd_etch,
                price.euro,
                price.euro_foil,
                price.tix
            FROM card_info.info AS info
            JOIN card_info.sets AS sets
                ON sets.set = info.set
            JOIN (
                SELECT
                    price.uri,
                    price.usd,
                    price.usd_foil,
                    price.usd_etch,
                    price.euro,
                    price.euro_foil,
                    price.tix,
                    price.date
                FROM card_data as price
                WHERE price.uri = %s
                ORDER BY date DESC
                LIMIT 1
                ) AS price
            ON price.uri = info.uri
            WHERE info.uri = %s

        """,
        (uri, uri),
    )

    data = cur.fetchall()
    conn.close()
    if data:
        response.status_code = status.HTTP_200_OK
        return CardInformation(
            status=response.status_code, data=parse_data_for_response(data)[0]
        )
    raise NotFound


@user_router.get("/buylinks/{set}/{col_num}/")
async def get_purchase_links(set: str, col_num: str, response: Response):
    # Update later
    conn, cur = connect_db()
    resp = cur.execute(
        "SELECT tcg_id FROM card_info.info WHERE set = %s AND id = %s",
        (
            set,
            col_num,
        ),
    )
    if resp:
        response.status_code = status.HTTP_200_OK
        return CardPurchaseLink(status=response.status_code, data=resp.fetchone())
    pass


@user_router.get(
    "/images/{set}/{col_num}/",
    response_class=FileResponse,
    status_code=status.HTTP_200_OK,
)
async def get_card_image(set: str, col_num: str):
    uri = get_card_from_set_id(set, col_num)
    folder_path = f"./preordain/images/{set}/"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    image_path = f"{folder_path}{uri}.jpg"
    if not os.path.exists(image_path):
        card_image = requests.request(
            method="GET",
            url=f"https://api.scryfall.com/cards/{set}/{col_num}?format=image",
            stream=True,
        )
        with open(image_path, "wb") as write_img:
            card_image.raw.decode_content = True
            shutil.copyfileobj(card_image.raw, write_img)

    return image_path
