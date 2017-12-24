from nuimo_menue.listener import *
from nuimo_openhab.app_builder import *
from nuimo_openhab.util import config

class Main:

    def __init__(self):
        try:
            self.run()
        except KeyboardInterrupt:
            self.exit_gracefully()


    def run(self):
        openhab = openHAB(config["openhab_api_url"])
        apps = OpenHabAppBuilder(openhab, config["openhab_sitemap"]).buildApps()

        manager = nuimo.ControllerManager(adapter_name=config["bluetooth_adapter"])
        manager.is_adapter_powered = True

        class ControllerManagerDiscoveryListener(nuimo.ControllerManagerListener):
            def __init__(self, main):
                self.main = main
            def controller_discovered(self, controller):
                self.main.controller = controller
                print("Discovered Nuimo controller:", controller.mac_address)
                if (controller.mac_address == str(config["nuimo_mac_address"]).lower()):
                    print("Found configured Nuimo with MAC address " + config["nuimo_mac_address"])
                    # Initialize App
                    menue = NuimoMenue(apps=apps, controller=controller)
                    controller.listener = NuimoMenueControllerListener(menue)
                    controller.connect()
                    menue.showIcon()
                else:
                    print("Discovered Nuimo " + controller.mac_address + " does not match with configured " + config[
                        "nuimo_mac_address"] + ". Continue discovery...")

        manager.listener = ControllerManagerDiscoveryListener(self)

        while (True):
            manager.start_discovery()
            manager.run()
            time.sleep(5)


    def exit_gracefully(self):
        if hasattr(self, 'controller'):
            print('Disconnecting...')
            self.controller.disconnect()
        sys.exit(0)


Main()