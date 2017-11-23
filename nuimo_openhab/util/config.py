import os
import sys
from nuimo_menue.config import NuimoMenueConfiguration
import yaml


class NuimoOpenHabConfiguration(NuimoMenueConfiguration):

    def __init__(self, config):
        super(NuimoOpenHabConfiguration, self).__init__(config["key_mapping"])
        self.config = config

    def __getitem__(self, item):
        return self.config[item]


NUIMO_OPENHAB_CONFIG_PATH = os.getenv('NUIMO_OPENHAB_CONFIG_PATH', 'config.yml')

with open(NUIMO_OPENHAB_CONFIG_PATH, 'r') as ymlfile:
    rawConfig = yaml.safe_load(ymlfile)
    print(rawConfig)
    sys.modules[__name__] = NuimoOpenHabConfiguration(rawConfig)
