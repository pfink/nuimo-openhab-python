from nuimo_menue.model import *
import nuimo_menue.icons
from nuimo_openhab.listener import *


class OpenHabAppBuilder:
    def __init__(self, openhab : openHAB, sitemapName = "nuimo"):
        self.openhab = openhab
        self.sitemapName = sitemapName
        self.rootItemName = "Nuimo"

    def buildApps(self):
        apps = []

        sitemap = self.openhab.req_get("/sitemaps/"+self.sitemapName)
        rootWidgets = sitemap["homepage"]["widgets"]
        for widget in rootWidgets:
            widgetApps = self.createAppFromWidget(widget)
            for app in widgetApps: apps.append(app)

        #nuimoRootItem = self.openhab.req_get("/items/"+self.rootItemName)

        #if (nuimoRootItem["type"] == "Group" and "members" in nuimoRootItem):
        #    for nuimoChildItem in nuimoRootItem["members"]:
        #        app = self.createAppFromItem(nuimoChildItem)
        #        apps.append(app)
        #else:
        #    app = self.createAppFromItem(nuimoRootItem)
        #    apps.append(app)

        return apps

    def createAppFromWidget(self, widget, parent: App = None):
        print("Test")
        apps = []
        print(widget["type"])
        # Ignore Frames
        if widget["type"] == "Frame":
            for childWidget in widget["widgets"]:
                childApps = self.createAppFromWidget(childWidget, parent)
                for app in childApps: apps.append(app)
        elif widget["type"] == "Group":
            item = self.openhab.req_get("/items/" + widget["item"]["name"])
            print(item)
            self.createAppFromItem(item, parent)
        elif widget["type"] == "Text":
            icon = self.resolveIcon(widget["label"], widget["icon"])
            app = App(name=widget["label"], appListener=OpenHabItemListener(self.openhab), icon=icon, parent=parent)
            for childWidget in widget["linkedPage"]["widgets"]:
                self.createAppFromWidget(childWidget, app)
            apps.append(app)
        else:
            if widget["type"] == "Switch" and widget["mappings"]:
                widget["type"] = "CustomSwitch"
            parent.getListener().addWidget(widget)

        return apps


    def createAppFromItem(self, nuimoItem, parent: App = None):
        print("Test")
        label = nuimoItem["label"] if "label" in nuimoItem else nuimoItem["name"]
        predefinedIcon = nuimoItem["category"] if "category" in nuimoItem else None
        icon = self.resolveIcon(label, predefinedIcon)
        itemListener = OpenHabItemListener(self.openhab)
        itemListener.addItem(nuimoItem)
        app = App(name=nuimoItem["name"], appListener=itemListener, icon=icon, parent=parent)

        if "members" in nuimoItem:
            for nuimoChildItem in nuimoItem["members"]:
                if(nuimoChildItem["type"] == "Group"):
                    self.createAppFromItem(nuimoChildItem, app)

        return app

    def resolveIcon(self, label, predefinedIcon = None):

        if len(label) == 81 and (
                "*" in label or "." in label):
            rawIcon = label
        elif predefinedIcon is not None and predefinedIcon in nuimo_menue.icons:
            rawIcon = nuimo_menue.icons[predefinedIcon]
        else:
            raise RuntimeError("No icon found for openHAB item '"+ label+"'")

        if(rawIcon is not None):
            if len(rawIcon) == 81:
                icon = nuimo.LedMatrix(rawIcon)
            else:
                raise RuntimeError("Icon for openHAB item '" + label + "' has an invalid length: "+ str(len(rawIcon)) +" (should be 81)")

        return icon
