from pydantic import BaseModel

class CardInfo(BaseModel):
    resp  : str
    status: int
    data: list

# * data usually refer to a certain set of data. see SaleDataSingleCardResponse class


# Example of data from Scryfall
"""
"object": "list",
  "total_cards": 1,
  "has_more": false,
  "data": [
    {
      "object": "card",
      "id": "31b770cc-09e7-4c0b-b2a4-462ab4f7200d",
      "oracle_id": "c7aecca5-2f67-4245-ab2d-e723d8b23a67",
      "set_name": "Strixhaven: School of Mages",
      ...
      "collector_number": "186",
      ...
      "preview": {
        "source": "Corocoro",
        "source_uri": "https://corocoro.jp/279032/",
        "previewed_at": "2021-03-30"
      },
      "prices": {
        "usd": "3.42",
        "usd_foil": "3.57",
        "usd_etched": null,
        "eur": "3.38",
        "eur_foil": "7.76",
        "tix": "0.26"
      },
      "related_uris": {
        ...
      },
      "purchase_uris": {
        ...
      }
    }
"""