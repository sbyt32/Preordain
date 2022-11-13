import configparser
import os


config = configparser.ConfigParser()
config.read('config.ini')

if not os.path.exists('config.ini') or os.path.exists('config.ini') and input("config.ini already exists, replace? y/n ").lower() in ["y", "yes"]:
    config['DEFAULT']           = {}
    config['CONNECT']           = {}
    config['DEFAULT']['path']   = ""
    config['DEFAULT']['config'] = "config.ini"
    config['CONNECT']["host"]   = input("Host Address: (Default: localhost) ") or "localhost"
    config['CONNECT']["user"]   = input("Username: ")
    config['CONNECT']["pass"]   = input(f"Password for {config['CONNECT']['user']}: ")
    config['CONNECT']["dbname"] = input("Database: (Default: price_tracker) ") or "price_tracker"
    with open('config.ini', 'w') as config_update:
        config.write(config_update)
else:
    print("Exiting setup...")