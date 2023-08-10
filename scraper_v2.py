import requests
import datetime
from sqlalchemy import MetaData, insert
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from preordain.v2.database import session


main_metadata = MetaData()


class PreordainBase(DeclarativeBase):
    pass


class SetTable(PreordainBase):
    __tablename__ = "sets"
    __table_args__ = {"schema": "card_information"}

    set_code: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    set_name: Mapped[str] = mapped_column(nullable=False)
    release_date: Mapped[datetime.date] = mapped_column()


for set in requests.get("https://api.scryfall.com/sets").json()["data"]:
    session.add(
        SetTable(
            set_code=set["code"], set_name=set["name"], release_date=set["released_at"]
        )
    )
session.commit()

# session.execute(
#     insert(SetTable)
#     .values("")
# )
# pass


# for sets in send_response("GET", "https://api.scryfall.com/sets")["data"]:
#     cur.execute(
#         """
#         INSERT INTO card_info.sets (set, set_full, release_date)
#         VALUES (%s, %s, %s)

#         ON CONFLICT DO NOTHING
#         """,
#         (sets["code"], sets["name"], sets["released_at"]),
#     )
# conn.commit()
# print("Hello, Sets are updated!")
