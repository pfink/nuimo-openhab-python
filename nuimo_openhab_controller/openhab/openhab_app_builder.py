from nuimo_openhab_controller.nuimomenue.model import *
from nuimo_openhab_controller.openhab.openhab_listener import *
import nuimo
from openhab import openHAB

class OpenHabAppBuilder:
    def buildApps(self, openhab : openHAB):
        apps = []
        nuimoGroupItem = openhab.req_get("/items/Nuimo")
        for nuimoItem in nuimoGroupItem["members"]:
            icon = nuimo.LedMatrix(
                nuimoItem["label"]
            )
            apps.append(App(name=nuimoItem["name"], appListener=OpenHabItemListener(openhab), icon=icon))
        return apps
