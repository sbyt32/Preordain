import configparser
import os
import hashlib
import logging
log = logging.getLogger()

def _gen_token():
    return hashlib.sha256().hexdigest()
def cfg_setup():
    cfg_folder_path = 'config_files/'
    if not os.path.exists(cfg_folder_path):
        os.makedirs(cfg_folder_path)

    # * A config file just to get some basic info and where other data is.
    cfg = configparser.ConfigParser()
    cfg.read(cfg_folder_path + 'config.ini')

    # TODO: Something with this
    cfg['FILE_DATA']                  = {}
    cfg['FILE_DATA']['db_exists']     = input("Create Database? y/n (Default: y) ") or "y"

    # Check if the database exists
    if cfg['FILE_DATA']['db_exists'] in ["yes", "y"]:
        cfg['FILE_DATA']['db_exists']  = "false"
    elif cfg['FILE_DATA']['db_exists'] in ["No", "n"]:
        cfg['FILE_DATA']['db_exists']  = "true"
    else:
        print("Invalid value, assuming database does not exist.")
        cfg['FILE_DATA']['db_exists']  = "false"

    # * A config file to hold connection information, mostly to pass into psycopg3 
    database = configparser.ConfigParser()
    database.read(cfg_folder_path + 'database.ini')

    database['CONNECT']                  = {}
    database['UPDATES']                  = {}
    database['UPDATES']['tcg_sales']     = "None"
    database['UPDATES']['price_fetch']   = "None"
    database['CONNECT']["host"]          = input("Host Address: (Default: localhost) ") or "localhost"
    database['CONNECT']["user"]          = input("Username: ")
    database['CONNECT']["password"]      = input(f"Password for {database['CONNECT']['user']}: ")
    database['CONNECT']["dbname"]        = input("Database: (Default: price_tracker) ") or "price_tracker"

    # * A config file for tokens! Tokens for general access, writing, and price data.
    tokens = configparser.ConfigParser()
    tokens.read(cfg_folder_path + 'tokens.ini')

    tokens['CONNECT']                    = {}
    log.info("Generating some tokens...")
    tokens['CONNECT']['sec_token']       = _gen_token()
    tokens['CONNECT']['write_token']     = _gen_token()
    tokens['CONNECT']['price_token']     = _gen_token()

    with open(cfg_folder_path + 'config.ini', 'w') as config_update:
        cfg.write(config_update)

    with open(cfg_folder_path + 'database.ini', 'w') as database_update:
        database.write(database_update)

    with open(cfg_folder_path + 'tokens.ini', 'w') as tokens_update:
        tokens.write(tokens_update)
