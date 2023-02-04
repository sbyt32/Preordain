# Primary script
# ! TO BE PHASED OUT, SEE fetch_card_data.py
import arrow
from scripts.fetch_price_data import query_price
from preordain.config_reader import read_config
import logging
import logging_details
logging_details.log_setup()
log = logging.getLogger()
log.setLevel(logging.INFO)


def main():
    cfg = read_config('FILE_DATA', 'config')
    if 'db_exists' not in cfg:
        log.error("Cannot confirm that the database exist. Does config_files/config.ini exist?")
        return
    else:
        if not bool(cfg['db_exists']):
            log.error("Database does not exist according to config_files/config.ini")
            return

        log.info(f"Fetching card data on {arrow.utcnow().format('YYYY-MM-DD')}")
        query_price()

if __name__ == "__main__":
    main()