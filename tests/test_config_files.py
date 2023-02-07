from preordain import config
# from scripts.check_if_update import check_date_to_update
class TestConfigFiles:

    # Test to see if the DB_EXISTS is a bool
    def test_config_ini(self):

        assert bool(config.DB_EXISTS)
