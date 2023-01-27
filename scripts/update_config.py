import configparser

def update_config(cfg:str, section:str, key:str, value) -> None:
    """
    Update a value in one of the config files. 
    Do NOT include the `.ini` in the name
    """
    config = configparser.ConfigParser()
    config.read(f'config_files/{cfg}.ini')
    config[section][key] = value
    with open(f'config_files/{cfg}.ini', 'w') as config_update:
        config.write(config_update)
