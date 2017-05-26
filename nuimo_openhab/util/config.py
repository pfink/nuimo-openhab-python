import yaml
import os
import sys

NUIMO_OPENHAB_CONFIG_PATH = os.getenv('NUIMO_OPENHAB_CONFIG_PATH', 'config.yml')

with open(NUIMO_OPENHAB_CONFIG_PATH, 'r') as ymlfile:
    config = yaml.safe_load(ymlfile)
    print(config)
    sys.modules[__name__] = config
