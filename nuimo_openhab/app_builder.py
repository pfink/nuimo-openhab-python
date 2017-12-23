from nuimo_menue.model import *
import nuimo_menue.icons
from nuimo_openhab.listener import *


class OpenHabAppBuilder:
    def __init__(self, openhab : openHAB, sitemapName = "nuimo"):
        self.openhab = openhab
        self.sitemapName = sitemapName

    def buildApps(self):
        apps = []

        sitemap = self.openhab.req_get("/sitemaps/"+self.sitemapName)
        rootWidgets = sitemap["homepage"]["widgets"]
        for widget in rootWidgets:
            widgetApps = self.createAppFromWidget(widget)
            for app in widgetApps: apps.append(app)

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
        elif widget["type"] == "Text" and "linkedPage" in widget or parent is None and widget["type"] in ["Switch", "Slider"]:
            icon = self.resolveIcon(widget["label"], widget["icon"])
            openhabListener = OpenHabItemListener(self.openhab)
            if widget["type"] != "Text":
                openhabListener.addWidget(widget)
            app = App(name=widget["label"], appListener=openhabListener, icon = icon, parent = parent)
            if "linkedPage" in widget:
                for childWidget in widget["linkedPage"]["widgets"]:
                    self.createAppFromWidget(childWidget, app)
            apps.append(app)
        elif widget["type"] in ["Switch", "Slider"]:
            if widget["mappings"]:
                widget["type"] = "CustomSwitch"
            parent.getListener().addWidget(widget)
        else:
            raise RuntimeError("Unsupported widget: "+widget["type"]+" '"+widget["label"]+"'")

        return apps

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
