from nuimo_menue.model import *
from nuimo_openhab.listener import *


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
