import yaml
import sys
import os

project_root_dir = os.path.dirname(sys.argv[0])

with open(os.path.join(project_root_dir, "led_icons", "9x9-led-icons.yml"), 'r') as ymlfile:
    sys.modules[__name__] = yaml.safe_load(ymlfile)