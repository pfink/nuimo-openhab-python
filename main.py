#!/usr/bin/python3
import signal
import threading
import traceback
import os
from nuimo_menue.listener import *
from nuimo_openhab.app_builder import *
from nuimo_openhab.util import config

class Main:

    def run(self):
        try:
            openhab = openHAB(config["openhab_api_url"])
            apps = OpenHabAppBuilder(openhab, config["openhab_sitemap"]).buildApps()

            manager = nuimo.ControllerManager(adapter_name=config["bluetooth_adapter"])
            manager.is_adapter_powered = True

            class ControllerManagerDiscoveryListener(nuimo.ControllerManagerListener):
                def __init__(self, main):
                    self.main = main
                def controller_discovered(self, controller):
                    self.main.controller = controller
                    logging.info("Discovered Nuimo controller: %s", controller.mac_address)
                    if (controller.mac_address == str(config["nuimo_mac_address"]).lower()):
                        logging.info("Found configured Nuimo with MAC address " + config["nuimo_mac_address"])
                        # Initialize App
                        menue = NuimoMenue(apps=apps, controller=controller)
                        controller.listener = NuimoMenueControllerListener(menue)
                        controller.connect()
                        menue.showIcon()
                    else:
                        logging.info("Discovered Nuimo " + controller.mac_address + " does not match with configured " + config[
                            "nuimo_mac_address"] + ". Continue discovery...")

            manager.listener = ControllerManagerDiscoveryListener(self)

            while (True):
                manager.start_discovery()
                manager.run()
                time.sleep(5)
        except Exception:
            logging.error(traceback.format_exc())


    def __init__(self):
        try:
            # Register graceful shutdown for all common termination requests
            for sig in [signal.SIGHUP, signal.SIGINT, signal.SIGTERM, signal.SIGABRT, signal.SIGQUIT]:
                signal.signal(sig, self.signal_handler)

            # We have run everything within a subthread because bitchy Python does not want to handle signals as everyone would expect
            # See also: https://bugs.python.org/issue5315
            self.thread = threading.Thread(target = self.run)
            self.thread.start()
            self.thread.join()
            self.exit_gracefully(1)
        except KeyboardInterrupt:            
            self.exit_gracefully()


    def signal_handler(self, *args):
        self.exit_gracefully()

    def exit_gracefully(self, exit_code = 0):
        logging.info('Shutting down gracefully...')
        if hasattr(self, 'controller') and self.controller.is_connected():
            logging.info('Disconnecting Nuimo...')
            self.controller.disconnect()
            logging.info('Nuimo disconnected!')
        logging.shutdown()
        os._exit(exit_code)


Main()