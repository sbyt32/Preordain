import configparser
import logging
log = logging.getLogger("config_reader")

def read_config(section:str, cfg:str):
    """A way to read and parse the different config files.
    Example = `read_config('CONNECT', 'config')`
| input   | desc                       |
|---------|----------------------------|
| section | header to get in .ini file |
| cfg     | .ini file name             | 
-------
    - config.ini
      - FILE_DATA
              - config_path `str`
              - token_path `str`
              - database_path `str`
              - db_exists `bool`
    - database.ini
      - CONNECT
              - host `str`
              - user `str`
              - password `str`
              - dbname `str`
      - UPDATES
              - tcg_sales `iso8601`
              - price_fetch `iso8601`
    - tokens.ini
      - CONNECT
              - sec_token `str`
              - write_token `str`
              - price_token `str`
    """


    parser = configparser.ConfigParser()
    cfg_file = f'config_files/{cfg}.ini'
    parser.read(cfg_file)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        db = dict(params)
    else:
        raise Exception(f'Section {section} not found in the {cfg_file} file')
    return db
