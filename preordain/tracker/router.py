import logging

log = logging.getLogger()
from preordain.utils.connections import connect_db, send_response
from preordain.utils.find_missing import validate_card_exists_from_uri
from preordain.exceptions import NotFound
from preordain.tracker.schema import CardInfoModel
from preordain.tracker.models import SuccessfulRequest

# from preordain.trackers.dependencies import duplicate_card
from fastapi import APIRouter, Response, status, Depends

router = APIRouter()

validate_query = """
    SELECT
        name, card_info.sets.set_full, id, scrape_sales
    FROM card_info.info
    JOIN card_info.sets
        ON card_info.sets.set = card_info.info.set
    WHERE uri = %s
"""


@router.post(
    "/add/",
    response_model=SuccessfulRequest,
    description="Add a card to get scraped by TCGPlayer (default is x1/wk)",
)
async def add_card_to_track(response: Response, card: CardInfoModel):
    card_dict = card.dict()
    if not validate_card_exists_from_uri(card_dict["uri"]):
        response.status_code = status.HTTP_400_BAD_REQUEST
        raise NotFound

    conn, cur = connect_db()

    query = """
        UPDATE card_info.info
        SET scrape_sales = 'true'
        WHERE uri = %s
    """
    cur.execute(query, (card_dict["uri"],))
    conn.commit()

    cur.execute(validate_query, (card_dict["uri"],))
    data = cur.fetchone()

    if data["scrape_sales"]:
        conn.close()
        response.status_code = status.HTTP_201_CREATED

        return SuccessfulRequest(
            status=response.status_code,
            info={"message": "Successfully stopped tracking"},
            data=card_dict,
        )


@router.post(
    "/remove/",
    response_model=SuccessfulRequest,
    description="Remove a card from having the sales scraped from TCGPlayer.",
)
async def remove_card_to_track(response: Response, card: CardInfoModel):
    card_dict = card.dict()
    conn, cur = connect_db()

    query = """
        UPDATE card_info.info
        SET scrape_sales = 'false'
        WHERE uri = %s
    """
    cur.execute(query, (card_dict["uri"],))
    conn.commit()

    cur.execute(validate_query, (card_dict["uri"],))
    data = cur.fetchone()

    if not data["scrape_sales"]:
        conn.close()
        response.status_code = status.HTTP_201_CREATED

        return SuccessfulRequest(
            status=response.status_code,
            info={"Successfully stopped tracking "},
            data=data,
        )
