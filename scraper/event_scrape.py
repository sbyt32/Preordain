import requests
from enum import Enum
from pydantic import BaseModel
from bs4 import BeautifulSoup
from .connections import connect_db
from datetime import datetime
import re


class FormatEnum(str, Enum):
    Standard = "ST"
    Pioneer = "PI"
    Modern = "MO"
    Legacy = "LE"
    Vintage = "VI"


class EventData(BaseModel):
    format: FormatEnum
    url: str
    event_name: str
    event_date: str  # Make a date value later xd
    event_type: str


FORMATS = ["ST", "PI", "MO", "LE", "VI"]

conn, cur = connect_db()

for format in FORMATS:
    site_data = requests.request("GET", f"http://mtgtop8.com/format?f={format}")
    if not site_data.ok:
        raise Exception("idk site down maybe, check ur internet? ( fill this in later)")
    soup = BeautifulSoup(site_data.text, "html.parser")

    for event_name, event_date, event_type in zip(
        soup.select("tr.hover_tr td.S14 a"),
        soup.select("tr.hover_tr td.S12"),
        soup.select("tr.hover_tr td:nth-child(1) img"),
    ):
        cur.execute(
            """
            INSERT INTO
                event_data.events
            VALUES ( %(format)s, %(url)s, %(event_name)s, %(event_date)s, %(event_type)s )
            ON CONFLICT DO NOTHING
            """,
            EventData(
                format=format,
                event_name=event_name.get_text(),
                event_date=datetime.strptime(
                    event_date.get_text(), "%d/%m/%y"
                ).strftime("%m/%d/%Y"),
                url=f'http://mtgtop8.com/{event_name.get("href")}',
                event_type=re.search(r"/([a-z]*).png$", event_type.get("src")).group(1)
                or "other",
            ).dict(),
        )

conn.commit()
