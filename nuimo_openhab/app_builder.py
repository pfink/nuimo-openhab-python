from nuimo_menue.model import *
import nuimo_menue.icons
import copy
from nuimo_openhab.listener import *


class OpenHabAppBuilder:
    def __init__(self, openhab : OpenHAB, sitemapName = "nuimo"):
        self.openhab = openhab
        self.sitemapName = sitemapName
        self.sitemap = dict()

    def fetch_sitemap(self):
        sitemap = self.openhab.req_get("/sitemaps/" + self.sitemapName)
        hasChanged = not self.compare_sitemap_config(sitemap, self.sitemap)
        if hasChanged:  logging.info("New/changed sitemap fetched: %s", sitemap)            
        else:           logging.debug("Fetched sitemap: %s", sitemap)
        self.sitemap = sitemap
        return hasChanged

    def fetch_apps(self):
        self.fetch_sitemap()
        return self.build_apps()

    def build_apps(self):
        apps = []

        rootWidgets = copy.deepcopy(self.sitemap["homepage"]["widgets"])
        for widget in rootWidgets:
            widgetApps = self.createAppFromWidget(widget)
            for app in widgetApps: apps.append(app)

        return apps

    def createAppFromWidget(self, widget, parent: App = None):
        apps = []
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

        if self.is_icon_label(label):
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

    def is_icon_label(self, label):
        return len(label) == 81 and (
                "*" in label or "." in label)

    def compare_sitemap_config(self, sitemap1, sitemap2):
        if isinstance(sitemap1, list) and isinstance(sitemap2, list) and len(sitemap1) == len(sitemap2):
            for index, value in enumerate(sitemap1):
                if not self.compare_sitemap_config(value, sitemap2[index]):
                    return False
        elif isinstance(sitemap1, dict) and isinstance(sitemap2, dict):
            for key, value in sitemap1.items():
                if key not in sitemap2 or key != "state" and (key != "label" or self.is_icon_label(value)) and not self.compare_sitemap_config(value, sitemap2[key]):
                    logging.debug("Sitemap configuration does not match. Value of key %s differs or key is not available in other sitemap", key)
                    return False
        elif not sitemap1 == sitemap2:
            logging.debug("Sitemap configuration is do not match. Value '%s' is differs from '%s", sitemap1, sitemap2)
            return False

        return True