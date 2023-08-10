import requests
import re
from sqlalchemy import insert
from preordain.v2.database import session
from preordain.v2.schema import SetTable, PriceTable, CardFormatTable

# Regex Pattern for Date
regex_pattern = re.compile(
    r"[0-9]{4}-[0-9]{2}-[0-9]{2}.*[0-9]{2}:[0-9]{2}:[0-9]{2}", re.IGNORECASE
)


# * Card Prices &
default_cards_data = requests.get(
    "https://api.scryfall.com/bulk-data/default_cards"
).json()
default_card_updated_at = (
    regex_pattern.search(default_cards_data["updated_at"])
    .group()
    .replace("T", "_")
    .replace(":", "")[0:10]
)


for card_data in requests.get(default_cards_data["download_uri"]).json():
    prices: dict[int | None] = card_data["prices"]
    session.add(
        PriceTable(
            scryfall_uri=card_data["id"],
            date=default_card_updated_at,
            usd=prices["usd"],
            usd_foil=prices["usd_foil"],
            usd_etch=prices.get("usd_etched", None),
            euro=prices["eur"],
            euro_foil=prices["eur_foil"],
            tix=prices["tix"],
        )
    )
    legalities = card_data["legalities"]
    session.add(
        CardFormatTable(
            scryfall_uri=card_data["id"],
            standard=legalities["standard"],
            historic=legalities["historic"],
            pioneer=legalities["pioneer"],
            modern=legalities["modern"],
            legacy=legalities["legacy"],
            pauper=legalities["pauper"],
            vintage=legalities["vintage"],
            commander=legalities["commander"],
        )
    )

# * Sets
# for set in requests.get("https://api.scryfall.com/sets").json()["data"]:
#     session.add(
#         SetTable(
#             set_code=set["code"], set_name=set["name"], release_date=set["released_at"]
#         )
#     )


session.commit()
