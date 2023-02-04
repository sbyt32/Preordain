from preordain.data_scraping.fetch_sale_data import fetch_tcg_prices
from preordain.data_scraping.fetch_price_data import query_price
from preordain.config_reader import read_config
from scripts.check_if_update import check_date_to_update
import arrow
import datetime
import logging
import logging_details


# ? Maybe move this to a config file! How would I put a timedelta tho in an .ini
# PRICE_CHECK should fetch data every 22 hours, which is around a day with some leeway.
PRICE_CHECK = datetime.timedelta(hours=22)
# SALE_CHECK should fetch data every 7 days, there's no need to update sale data constantly.
SALE_CHECK  = datetime.timedelta(days=7)

def main():
    logging_details.log_setup()
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)

    cfg = read_config('FILE_DATA', 'config')
    if 'db_exists' not in cfg:
        log.error("Cannot confirm that the database exist. Does config_files/config.ini exist?")
        return
    if not bool(cfg['db_exists']):
        log.error('yap')
        return
        
    date_to_compare = read_config('UPDATES', 'database')
    data_stuff = dict(zip(date_to_compare,[PRICE_CHECK,SALE_CHECK]))

    for file, date_stuff in data_stuff.items(): 
        if check_date_to_update(date_to_compare[file], date_stuff):
            if file == 'tcg_sales':
                log.info(f"Fetching card data on {arrow.utcnow().format('YYYY-MM-DD')}")
                query_price()
            elif file == 'price_fetch':
                log.info(f"Fetching sale data on {arrow.utcnow().format('YYYY-MM-DD')}")
                fetch_tcg_prices() 

if __name__ == '__main__':
    main()
