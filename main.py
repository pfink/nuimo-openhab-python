from nuimo_openhab_controller.nuimomenue.listener import *
from nuimo_openhab_controller.nuimomenue.model import *
from nuimo_openhab_controller.openhab.openhab_listener import *
from nuimo_openhab_controller.openhab.openhab_app_builder import *

'''
apps = []

apps.append(App(appListener=OpenHabItemListener(), name="App 1", icon= nuimo.LedMatrix(
    "*       *"
    " *     * "
    "  *   *  "
    "   * *   "
    "    *    "
    "   * *   "
    "  *   *  "
    " *     * "
    "*       *"
)))

apps.append(App(appListener=OpenHabItemListener(), name="App 2", icon= nuimo.LedMatrix(
    "*********"
    "         "
    "         "
    "         "
    "         "
    "   * *   "
    "  *   *  "
    " *     * "
    "*       *"
)))


apps.append(App(appListener=OpenHabItemListener(), name="App 3", icon= nuimo.LedMatrix(
    "*********"
    "         "
    "         "
    "         "
    "         "
    "         "
    "         "
    "         "
    "*********"
)))

openhab
'''

apps = OpenHabAppBuilder().buildApps()

manager = nuimo.ControllerManager(adapter_name='hci0')
controller = nuimo.Controller(mac_address='E3:CF:57:6A:78:3E', manager=manager)
menue = NuimoMenue(apps=apps, controller=controller)
# Register listener
controller.listener = NuimoMenueControllerListener(menue)
controller.connect()


menue.showIcon()
manager.run()