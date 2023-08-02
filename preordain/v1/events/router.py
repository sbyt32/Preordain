from fastapi import APIRouter, Response, status
from cachetools import cached, TTLCache
from preordain.utils.get_last_update import to_tomorrow
from preordain.utils.connections import connect_db
from .models import EventListings
from .enums import EventFormat

router = APIRouter()


@cached(cache=TTLCache(maxsize=1024, ttl=to_tomorrow()))
@router.get("/", description="Get the last 10 events of a specific format.")
async def get_recent_events(
    response: Response, format: EventFormat = EventFormat.Standard
):
    conn, cur = connect_db()

    cur.execute(
        """
        SELECT
            format,
            url,
            event_name,
            event_date,
            event_type
        FROM event_data.events
        WHERE format = %s
        ORDER BY event_date DESC
        LIMIT 10
    """,
        (format,),
    )

    data = cur.fetchall()
    if data:
        response.status_code = status.HTTP_200_OK
        return EventListings(status=response.status_code, data=data)
