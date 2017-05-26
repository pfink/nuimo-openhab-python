from nuimo_menue.listener import *
from nuimo_openhab.app_builder import *
from nuimo_openhab.util import config

openhab = openHAB(config["openhab_api_url"])
apps = OpenHabAppBuilder().buildApps(openhab)

manager = nuimo.ControllerManager(adapter_name='hci0')
controller = nuimo.Controller(mac_address=config["nuimo_mac_address"], manager=manager)
menue = NuimoMenue(apps=apps, controller=controller)
# Register listener
controller.listener = NuimoMenueControllerListener(menue)

while(True):
    controller.connect()
    menue.showIcon()
    manager.run()
    time.sleep(5)