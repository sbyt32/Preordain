from sqlalchemy import (
    create_engine,
    select,
    Table,
    MetaData,
    Column,
    Text,
    String,
    Boolean,
)
from sqlalchemy.dialects.postgresql import ARRAY

main_metadata = MetaData()

card_index = Table(
    "card_key_index",
    main_metadata,
    Column("scryfall_uri", String(255), nullable=False),
    Column("uniq_id", Text, nullable=False),
    Column("set_code", Text, nullable=False),
    Column("group", ARRAY(Text)),
    Column("tcg_id", Text),
    Column("tcg_id_etched", Text),
    Column("new_search", Boolean, default=True),
    Column("scraper", Boolean, default=False),
)
