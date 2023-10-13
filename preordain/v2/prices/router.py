from fastapi import APIRouter
from preordain.v2.database import session
from preordain.v2.schema import PriceTable, CardMetadataTable, CardIndex
from preordain.v2.prices.models import PriceData
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import aliased

price_router = APIRouter()

price_cls = aliased(PriceTable, name="prices")
metadata_cls = aliased(CardMetadataTable, name="card_data")


@price_router.get("/{set_code}/{collector_number}", response_model=list[PriceData])
async def get_card_prices(set_code: str, collector_number: str, days: int = 30):
    if days > 30:
        days = 30

    result = session.execute(
        select(price_cls)
        .where(metadata_cls.set_code == set_code)
        .where(metadata_cls.collector_number == collector_number)
        .join(CardIndex.prices)
        .where(CardIndex.scryfall_uri == price_cls.scryfall_uri)
        .join(CardIndex.card_metadata)
        .where(CardIndex.scryfall_uri == metadata_cls.scryfall_uri)
        .distinct(price_cls.date)
        .order_by(price_cls.date.desc())
        .limit(days)
    )

    price_data = []
    for info in jsonable_encoder(result.mappings().fetchall()):
        prices = info["prices"]
        price_data.append(
            {
                "date": prices["date"],
                "prices": {
                    "usd": prices["usd"],
                    "usd_foil": prices["usd_foil"],
                    "usd_etch": prices["usd_etch"],
                    "euro": prices["euro"],
                    "euro_foil": prices["euro_foil"],
                    "tix": prices["tix"],
                },
            }
        )

    return price_data
