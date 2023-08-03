from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Text,
    String,
    Boolean,
    Float,
    Date,
    Enum,
    FLOAT,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
    DeclarativeBase,
    Mapped,
    Session,
)
import datetime

main_metadata = MetaData()


class MainBase(DeclarativeBase):
    pass


class CardIndex(MainBase):
    __tablename__ = "card_key_index"

    scryfall_uri: Mapped[str] = mapped_column(primary_key=True)
    uniq_id: Mapped[str] = mapped_column(nullable=False)
    card_id: Mapped[str] = mapped_column(nullable=False)
    groups: Mapped[list[str]] = mapped_column(ARRAY(String))
    tcg_id: Mapped[str] = mapped_column()
    tcg_id_etched: Mapped[str] = mapped_column()
    new_search: Mapped[bool] = mapped_column(default=True)
    scraper: Mapped[bool] = mapped_column(default=False)


price_metadata = MetaData("card_price_data")


class CardPriceDataBase(DeclarativeBase):
    __table_args__ = {"schema": "card_price_data"}


class PriceTable(CardPriceDataBase):
    __tablename__ = "price"
    scryfall_uri: Mapped[str] = mapped_column(primary_key=True)
    date: Mapped[datetime.date] = mapped_column()
    usd: Mapped[float] = mapped_column()
    usd_foil: Mapped[float] = mapped_column(FLOAT(2))
    usd_etch: Mapped[float] = mapped_column(FLOAT(2))
    euro: Mapped[float] = mapped_column(FLOAT(2))
    euro_foil: Mapped[float] = mapped_column(FLOAT(2))
    tix: Mapped[float] = mapped_column(FLOAT(2))


# price_table = Table(
#     "price",
#     price_metadata,
#     Column("scryfall_uri", Text, nullable=False, primary_key=True),
#     Column("date", Date),
#     Column("usd", Float(2)),
#     Column("usd_foil", Float(2)),
#     Column("usd_etch", Float(2)),
#     Column("euro", Float(2)),
#     Column("euro_foil", Float(2)),
#     Column("tix", Float(2)),
# )

# card_information_metadata = MetaData("card_information")

# card_format_table = Table(
#     "formats",
#     card_information_metadata,
#     Column("uniq_id", Text, nullable=False),
#     Column("standard", Enum(FormatLegalities), nullable=False),
#     Column("historic", Enum(FormatLegalities), nullable=False),
#     Column("pioneer", Enum(FormatLegalities), nullable=False),
#     Column("modern", Enum(FormatLegalities), nullable=False),
#     Column("legacy", Enum(FormatLegalities), nullable=False),
#     Column("pauper", Enum(FormatLegalities), nullable=False),
#     Column("vintage", Enum(FormatLegalities), nullable=False),
#     Column("commander", Enum(FormatLegalities), nullable=False)
# )

# card_set_table = Table(
#     "sets",
#     card_information_metadata,
#     Column("set_code", String(12), nullable=False, primary_key=True),
#     Column("set_name", Text, nullable=False),
#     Column("release_date", Date)
# )
