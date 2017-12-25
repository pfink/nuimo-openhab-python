import os
import sys
import logging
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

    loggers = []
    if rawConfig["log_file"]: loggers.append(logging.FileHandler(filename=rawConfig["log_file"]))
    if rawConfig["log_stdout"]: loggers.append(logging.StreamHandler(stream=sys.stdout))
    formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                                  "%Y-%m-%d %H:%M:%S")
    for logger in loggers: logger.setFormatter(formatter)
    if loggers: logging.basicConfig(handlers=loggers, level=rawConfig["log_level"])

    logging.info("Loaded config file from "+ NUIMO_OPENHAB_CONFIG_PATH)
    sys.modules[__name__] = NuimoOpenHabConfiguration(rawConfig)
