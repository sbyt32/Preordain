def parse_data_for_response(data: list):
    """
    Parse the data you recieved for this format.
    """
    card_data = []
    for cards in data:
        card_data.append(
            {
                'name': cards['name'],
                'set': cards['set'],
                'set_full': cards['set_full'],
                'id': cards['id'],
                'last_updated': cards['last_updated'],
                'prices': {
                    'usd': cards['usd'],
                    'usd_foil': cards['usd_foil'],
                    'euro': cards['euro'],
                    'euro_foil': cards['euro_foil'],
                    'tix': cards['tix'],
                }
            }
        )
    return card_data