import os
from exceptions import NoConfigFile
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser


CONFIG_FILE = '~/.gf-dispatcher-config'


def load_dispatcher_config():
    """..."""
    config = ConfigParser()
    config_filepath = os.path.expanduser(CONFIG_FILE)

    if os.path.isfile(config_filepath):
        config.read(config_filepath)
        credentials = config.items('Credentials')
        return {k:v for k,v in credentials}
    raise NoConfigFile(CONFIG_FILE)


SETTINGS = load_dispatcher_config()
