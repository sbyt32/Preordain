import os
import ndjson
import scripts

def query_price():
    with open('data/cards_to_query.ndjson', 'r') as card_database:
        cards_to_query = ndjson.reader(card_database)

        for cards in cards_to_query:
            card_name = cards['name']
            card_set = cards['set']
            card_id = cards['id']
            file_path = f'data/tracking/{card_set}/{card_id}_{scripts.util_sanitize_string(card_name)}.csv'

            if not os.path.exists(f'data/tracking/{card_set}'):
                os.makedirs(f'data/tracking/{card_set}')
            r = scripts.util_send_response(cards['uri'])
            scripts.query_add_data(r, file_path)
    # for cards in cards_to_query:
    #     card_name = cards['name']
    #     card_set = cards['set']
    #     card_id = cards['id']
    #     file_path = f'trackings/{card_set}/{card_id}_{scripts.util.sanitize_string(card_name)}'
    #     if not os.path.exists(f'tracking/{card_set}'):
    #         # ? Make a log here for making the folder
    #         os.makedirs(f'tracking/{card_set}')
    #     r = scripts.util.send_response(cards['uri'])
    #     scripts.query_price.append_cards(r, file_path)