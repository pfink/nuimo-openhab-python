from nuimo_openhab_controller.nuimomenue.listener import *
from nuimo_openhab_controller.nuimomenue.model import *
from nuimo_openhab_controller.openhab.openhab_listener import *
from nuimo_openhab_controller.openhab.openhab_app_builder import *
import time
from nuimo_openhab_controller import config
from openhab import openHAB


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