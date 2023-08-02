from preordain.search.models import CardSearchData


def parse_data_for_response(data: list):
    """
    Parse the data you recieved for this format.
    """
    card_data = []
    for card in data:
        card_data.append(
            CardSearchData(
                name=card["name"],
                set=card["set"],
                set_full=card["set_full"],
                id=card["id"],
                uri=card["uri"],
                scrape_sales=card["scrape_sales"] or False,
                last_updated=card["last_updated"],
                prices={
                    "usd": card["usd"],
                    "usd_foil": card["usd_foil"],
                    "usd_etch": card["usd_etch"],
                    "euro": card["euro"],
                    "euro_foil": card["euro_foil"],
                    "tix": card["tix"],
                },
            ).dict()
        )
    return card_data
