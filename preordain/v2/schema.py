from sqlalchemy import (
    create_engine,
    select,
    Table,
    MetaData,
    Column,
    Text,
    String,
    Boolean,
    Float,
    Date,
)
from sqlalchemy.dialects.postgresql import ARRAY

main_metadata = MetaData()

card_index = Table(
    "card_key_index",
    main_metadata,
    Column("scryfall_uri", String(255), nullable=False),
    Column("uniq_id", Text, nullable=False),
    Column("card_id", Text, nullable=False),
    Column("groups", ARRAY(Text)),
    Column("tcg_id", Text),
    Column("tcg_id_etched", Text),
    Column("new_search", Boolean, default=True),
    Column("scraper", Boolean, default=False),
)

price_metadata = MetaData("card_price_data")

price_table = Table(
    "price",
    price_metadata,
    Column("scryfall_uri", Text, nullable=False, primary_key=True),
    Column("date", Date),
    Column("usd", Float(2)),
    Column("usd_foil", Float(2)),
    Column("usd_etch", Float(2)),
    Column("euro", Float(2)),
    Column("euro_foil", Float(2)),
    Column("tix", Float(2)),
)
