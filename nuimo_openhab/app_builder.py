from nuimo_menue.model import *
import nuimo_menue.icons
from nuimo_openhab.listener import *


class OpenHabAppBuilder:
    def __init__(self, openhab : openHAB):
        self.openhab = openhab
        self.rootItemName = "Nuimo"

    def buildApps(self):
        apps = []
        nuimoRootItem = self.openhab.req_get("/items/"+self.rootItemName)

        if (nuimoRootItem["type"] == "Group" and "members" in nuimoRootItem):
            for nuimoChildItem in nuimoRootItem["members"]:
                app = self.createAppFromItem(nuimoChildItem)
                apps.append(app)
        else:
            app = self.createAppFromItem(nuimoRootItem)
            apps.append(app)

        return apps

    def createAppFromItem(self, nuimoItem, parent: App = None):
        icon = self.fetchIconFromItem(nuimoItem)
        app = App(name=nuimoItem["name"], appListener=OpenHabItemListener(self.openhab), icon=icon, parent=parent)

        if (nuimoItem["type"] == "Group" and "members" in nuimoItem):
            for nuimoChildItem in nuimoItem["members"]:
                self.createAppFromItem(nuimoChildItem, app)

        return app

    def fetchIconFromItem(self, nuimoItem):
        icon = None
        rawIcon = None

        if "label" in nuimoItem and len(nuimoItem["label"]) == 81 and (
                "*" in nuimoItem["label"] or "." in nuimoItem["label"]):
            rawIcon = nuimoItem["label"]
        elif "category" in nuimoItem and nuimoItem["category"] in nuimo_menue.icons:
            rawIcon = nuimo_menue.icons[nuimoItem["category"]]
        elif nuimoItem["type"] == "Group" and nuimoItem["name"] != self.rootItemName:
            raise RuntimeError("No icon found for openHAB item '"+ nuimoItem["name"]+"'")

        if(rawIcon is not None):
            if len(rawIcon) == 81:
                icon = nuimo.LedMatrix(rawIcon)
            else:
                raise RuntimeError("Icon for openHAB item '" + nuimoItem["name"] + "' has an invalid length: "+ str(len(rawIcon)) +" (should be 81)")

        return icon
