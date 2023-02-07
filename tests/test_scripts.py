from scripts.check_if_update import check_date_to_update
from scripts.update_config import update_config
from preordain.config_reader import read_config
import pytest
from datetime import timedelta


class TestScriptsFolder:

    def test_check_date_to_update_success(self):
        price = "2023-01-19 06:04:27.236195+00:00"
        sales = "2023-01-19 06:04:27.236195+00:00"

        # These should be True
        assert check_date_to_update(price, timedelta(days=1))
        assert check_date_to_update(sales, timedelta(days=7))
        
        # Check if it is set to None, as some data can be set to None.
        never_updated = "None"
        assert check_date_to_update(never_updated, timedelta(days=7))
    

    def test_check_date_to_update_fail(self):
        # These should fail, normal circumstances
        price_fail = ("2023-01-19 06:04:27.236195+00:00", "2023-01-19 06:04:27.236195+00:00")
        assert check_date_to_update(price_fail[0], timedelta(days=1), price_fail[1]) == False

        # This one should raise a TypeError.
        bad_value = None
        with pytest.raises(TypeError):
            check_date_to_update(bad_value, timedelta(days=7))

        # This is a format fail. date_format_fail is written in an incorrect format
        date_format_fail = ("2023-01-19 06:04:27.236195+00:00","2023-01-19 06:04:27")
        with pytest.raises(Exception):
            check_date_to_update(date_format_fail[0], timedelta(1), date_format_fail[1])

        with pytest.raises(Exception):
            check_date_to_update(date_format_fail[1], timedelta(1), date_format_fail[0])

    # TODO: This function, so far, edits an existing config file. This will not function
    # def test_cfg_update(self):
    #     update_config("tokens", "CONNECT", "sec_token", "hello")

    #     cfg = read_config("CONNECT", "tokens")
    #     assert cfg['sec_token'] == "hello"