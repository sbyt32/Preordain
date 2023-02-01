# for tye custom row factory
from api_files.models import BaseResponse, CardInformation, RespStrings
from datetime import date
class TestRowFactory:

    def test_dictrowfactory(self):

        svr = [{
            "name": "Thalia, Guardian of Thraben",
            "set": "vow",
            "set_full": "Innistrad: Crimson Vow",
            "id": "38",
            "last_updated": "2023-01-05",
            "usd": 0.92,
            "usd_foil": 3.05,
            "euro": 0.87,
            "euro_foil": 2.95,
            "tix": 0.17
            }]

        expected_resp = {
                'resp': RespStrings.card_info,
                'status': 200,
                'data': [
                    {
                        'name': 'Thalia, Guardian of Thraben',
                        'set': 'vow',
                        'set_full': 'Innistrad: Crimson Vow',
                        'id': '38',
                        'last_updated': date(2023, 1, 5),
                        'prices': {
                            'usd': 0.92,
                            'usd_foil': 3.05,
                            'euro': 0.87,
                            'euro_foil': 2.95,
                            'tix': 0.17
                        }
                    }
                ]
            }

        # This is the actual function of testing
        fields = [k for k in svr[0].keys()]
        values = [v for v in svr[0].values()]
        dict_format = {'prices': {}}
        for key in fields:
            if key in ['usd','usd_foil','euro','euro_foil','tix']:
                dict_format['prices'][key] =  dict_format.get(key, None)
            else:
                dict_format[key] = dict_format.get(key, key)

        card_info_data = dict(zip(fields[:5], values[:5]))
        card_info_prices = dict(zip(fields[5:], values[5:]))

        dict_format['prices'].update(card_info_prices)
        dict_format.update(card_info_data)


        assert BaseResponse[CardInformation](data=[dict_format], resp='card_info', status=200).dict() == expected_resp