from preordain.v1.information.models import InformationData


# To Do, add group info into groups.
def parse_data_for_response(data: list[InformationData]):
    """
    Parse the data you recieved for this format.
    """
    card_data = []
    for cards in data:
        card_data.append(
            InformationData(
                name=cards["name"],
                set=cards["set"],
                set_full=cards["set_full"],
                id=cards["id"],
                last_updated=cards["date"],
                uri=cards["uri"],
                prices={
                    "usd": cards["usd"],
                    "usd_foil": cards["usd_foil"],
                    "usd_etch": cards["usd_etch"],
                    "euro": cards["euro"],
                    "euro_foil": cards["euro_foil"],
                    "tix": cards["tix"],
                },
            ).dict()
        )

    return card_data
