import yaml
import sys

with open("led_icons/9x9-led-icons.yml", 'r') as ymlfile:
    sys.modules[__name__] = yaml.safe_load(ymlfile)