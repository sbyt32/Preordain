from sqlalchemy import MetaData, String, FLOAT, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
    DeclarativeBase,
    Mapped,
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

    prices: Mapped[list["PriceTable"]] = relationship(back_populates="card")
    card_metadata: Mapped[list["CardMetadataTable"]] = relationship(
        back_populates="card"
    )


class CardMetadataTable(MainBase):
    __tablename__ = "metadata"
    __table_args__ = {"schema": "card_information"}

    scryfall_uri: Mapped[str] = mapped_column(
        ForeignKey("card_key_index.scryfall_uri"), primary_key=True
    )
    card_name: Mapped[str] = mapped_column(default=None)
    set_code: Mapped[str] = mapped_column(default=None)
    collector_number: Mapped[str] = mapped_column(default=None)
    mana_cost: Mapped[str] = mapped_column(default=None)
    oracle_text: Mapped[str] = mapped_column(default=None)
    artist: Mapped[str] = mapped_column(default=None)

    card: Mapped["CardIndex"] = relationship(back_populates="card_metadata")


class PriceTable(MainBase):
    __tablename__ = "price"
    __table_args__ = {"schema": "card_price_data"}

    scryfall_uri: Mapped[str] = mapped_column(
        ForeignKey("card_key_index.scryfall_uri"), primary_key=True
    )
    date: Mapped[datetime.date] = mapped_column(primary_key=True)
    usd: Mapped[float] = mapped_column()
    usd_foil: Mapped[float] = mapped_column(FLOAT(2))
    usd_etch: Mapped[float] = mapped_column(FLOAT(2))
    euro: Mapped[float] = mapped_column(FLOAT(2))
    euro_foil: Mapped[float] = mapped_column(FLOAT(2))
    tix: Mapped[float] = mapped_column(FLOAT(2))

    card: Mapped["CardIndex"] = relationship(back_populates="prices")

    # def __repr__(self) -> str:
    #     return f"<PriceTable ('{self.date}', '{self.usd}', '{self.usd_foil}', '{self.usd_etch}', '{self.euro}', '{self.euro_foil}', '{self.tix}')>"
    # return super().__repr__()
