from fastapi import APIRouter, Response, status
from preordain.utils.connections import connect_db
from preordain.utils.parsers import parse_data_for_response
from .models import (
    CardInformation,
    CardPurchaseLink,
    CardMetadata,
    MetadataData,
)
from ..images.enums import ImageTypes
from ..images.utils import get_img_path
from preordain.v1.models import CardFormats
from preordain.v1.exceptions import NotFound
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
async def get_card_image(set: str, col_num: str, type: ImageTypes = ImageTypes.cards):
    return get_img_path(set, col_num, type)


@user_router.get("/metadata/{set}/{col_num}/", status_code=status.HTTP_200_OK)
async def get_card_metadata(set: str, col_num: str, response: Response):
    uri = get_card_from_set_id(set, col_num)
    conn, cur = connect_db()

    cur.execute(
        """
        SELECT
            info.name,
            info.set,
            sets.set_full,
            info.id,
            metadata.rarity,
            metadata.mana_cost,
            metadata.oracle_text,
            metadata.artist,
            formats.standard,
            formats.historic,
            formats.pioneer,
            formats.modern,
            formats.legacy,
            formats.pauper,
            formats.vintage,
            formats.commander
        FROM card_info.info AS info
        JOIN card_info.metadata AS metadata
            ON info.uri = metadata.uri
        JOIN card_info.formats AS formats
            ON info.uri = formats.uri
        JOIN card_info.sets AS sets
            ON info.set = sets.set
        WHERE info.uri = %s
        LIMIT 1
    """,
        (uri,),
    )

    data = cur.fetchone()
    return CardMetadata(
        status=200,
        data=MetadataData(
            name=data["name"],
            set=data["set"],
            set_full=data["set_full"],
            id=data["id"],
            rarity=data["rarity"],
            mana_cost=data["mana_cost"],
            oracle_text=data["oracle_text"],
            artist=data["artist"],
            legality=CardFormats(
                standard=data["standard"],
                historic=data["historic"],
                pioneer=data["pioneer"],
                modern=data["modern"],
                legacy=data["legacy"],
                pauper=data["pauper"],
                vintage=data["vintage"],
                commander=data["commander"],
            ),
        ),
    )
