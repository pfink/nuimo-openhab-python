from nuimo_menue.model import *
from nuimo_openhab.listener import *


class OpenHabAppBuilder:
    def buildApps(self, openhab : openHAB, rootItemName = "Nuimo", parent: App = None):
        apps = []
        nuimoGroupItem = openhab.req_get("/items/"+rootItemName)
        for nuimoItem in nuimoGroupItem["members"]:
            if("label" in nuimoItem):
                icon = nuimo.LedMatrix(
                    nuimoItem["label"]
                )
            app = App(name=nuimoItem["name"], appListener=OpenHabItemListener(openhab), icon=icon, parent=parent)
            if(nuimoItem["type"] == "Group"):
                self.buildApps(openhab, nuimoItem["name"], app)
            apps.append(app)
        return apps
