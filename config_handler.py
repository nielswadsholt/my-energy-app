from configparser import ConfigParser   

def read_from_config(key, section='DEFAULT') -> str:
    config = ConfigParser()
    config.read('config.ini')

    return config[section][key]

def write_to_config(key, value, section='DEFAULT') -> None:
    config = ConfigParser()
    config.read('config.ini')

    if section != 'DEFAULT' and not config.has_section(section):
        config.add_section(section)
    
    config[section][key] = value

    with open('config.ini', 'w') as config_file:
        config.write(config_file)