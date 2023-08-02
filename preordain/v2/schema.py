from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Text,
    String,
    Boolean,
    Float,
    Date,
    Enum
)
from sqlalchemy.dialects.postgresql import ARRAY
from preordain.v2.enums import FormatLegalities


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

card_information_metadata = MetaData("card_information")

card_format_table = Table(
    "formats",
    card_information_metadata,
    Column("uniq_id", Text, nullable=False),
    Column("standard", Enum(FormatLegalities), nullable=False),
    Column("historic", Enum(FormatLegalities), nullable=False),
    Column("pioneer", Enum(FormatLegalities), nullable=False),
    Column("modern", Enum(FormatLegalities), nullable=False),
    Column("legacy", Enum(FormatLegalities), nullable=False),
    Column("pauper", Enum(FormatLegalities), nullable=False),
    Column("vintage", Enum(FormatLegalities), nullable=False),
    Column("commander", Enum(FormatLegalities), nullable=False)
)

card_set_table = Table(
    "sets",
    card_information_metadata,
    Column("set_code", String(12), nullable=False, primary_key=True),
    Column("set_name", Text, nullable=False),
    Column("release_date", Date)
)