import logging

log = logging.getLogger()
from preordain.utils.connections import connect_db, send_response
from preordain.trackers.schema import CardInfoModel
from preordain.trackers.models import SuccessfulRequest

# from preordain.trackers.dependencies import duplicate_card
from fastapi import APIRouter, Response, status, Depends

router = APIRouter()


@router.post(
    "/add/",
    response_model=SuccessfulRequest,
    description="Add a card to get scraped by TCGPlayer (default is x1/wk)",
)
async def add_card_to_track(response: Response, card: CardInfoModel):
    card_dict = card.dict()
    conn, cur = connect_db()

    query = """
        UPDATE card_info.info
        SET scrape_sales = 'true'
        WHERE uri = %s
    """
    cur.execute(query, (card_dict["uri"],))
    conn.commit()
    conn.close()
    response.status_code = status.HTTP_201_CREATED

    return SuccessfulRequest(status=response.status_code, data=card)


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
    conn.close()
    response.status_code = status.HTTP_201_CREATED

    return SuccessfulRequest(status=response.status_code, data=card)
