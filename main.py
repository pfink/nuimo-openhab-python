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
            self.openhab = openHAB(config["openhab_api_url"])
            self.app_builder = OpenHabAppBuilder(self.openhab, config["openhab_sitemap"])

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
                        self.main.app_builder.fetch_sitemap()
                        self.main.initialize_controller()
                        if(config["openhab_autoupdate_sitemap"]):
                            self.main.initialize_updatethead()
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

    def apply_sitemap_changes(self):
        sitemapHasChanged = self.app_builder.fetch_sitemap()
        if sitemapHasChanged:
            self.initialize_controller()
        self.initialize_updatethead()

    def initialize_controller(self):
        apps = self.app_builder.build_apps()
        menue = NuimoMenue(apps=apps, controller=self.controller)
        self.controller.listener = NuimoMenueControllerListener(menue)
        if not self.controller.is_connected():
            self.controller.connect()
        menue.showIcon()
        logging.info("Controller and Listener (re-)initialized!")

    def initialize_updatethead(self):
        threading.Timer(config["openhab_autoupdate_sitemap"], self.apply_sitemap_changes).start()

    def __init__(self):
        try:
            # Register graceful shutdown for all common termination requests
            for sig in [signal.SIGHUP, signal.SIGINT, signal.SIGTERM, signal.SIGABRT, signal.SIGQUIT]:
                signal.signal(sig, self.signal_handler)

            # We have run everything within a subthread because bitchy Python does not want to handle signals as everyone would expect
            # See also: https://bugs.python.org/issue5315
            thread = threading.Thread(target = self.run)
            thread.start()
            thread.join()
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