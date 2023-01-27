from scripts.config_reader import read_config
from scripts.check_if_update import check_date_to_update
class TestConfigFiles:

    # Test to see if the DB_EXISTS is a bool
    def test_config_ini(self):
        cfg = read_config("FILE_DATA", "config")

        assert bool(cfg['db_exists'])
