from nuimo_openhab_controller.nuimomenue.model import *
from nuimo_openhab_controller.openhab.openhab_listener import *
import nuimo
import requests

class OpenHabAppBuilder:
    def buildApps(self):
        apps = []
        nuimoGroupItem = requests.get("http://192.168.0.31:8080/rest/items/Nuimo").json()
        for nuimoItem in nuimoGroupItem["members"]:
            icon = nuimo.LedMatrix(
                nuimoItem["label"] +
                "         "
                "         "
                "         "
                "         "
                "   * *   "
                "  *   *  "
                " *     * "
                "*       *"
            )
            apps.append(App(name=nuimoItem["name"], appListener=OpenHabItemListener(), icon=icon))
        return apps
